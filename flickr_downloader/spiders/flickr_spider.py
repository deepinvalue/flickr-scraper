from urllib.parse import urlencode
from pathlib import Path
import json
import scrapy
from ..items import FlickrDownloaderItem

class FlickrSpider(scrapy.Spider):
    name = 'flickr'
    allowed_domains = ['flickr.com', 'live.staticflickr.com']

    def __init__(self, *args, **kwargs):
        super(FlickrSpider, self).__init__(*args, **kwargs)
        with open('config.json') as config_file:
            config = json.load(config_file)
            self.api_key = config['api_key']
            self.categories = {category: data['tags'] for category, data in config['categories'].items()}
            self.images_store = config['images_store']
            self.total_photos_limits = {category: data['total_photos_limit'] for category, data in config['categories'].items()}
        self.downloaded_files = {category: set() for category in self.categories.keys()}            
    
    def start_requests(self):
        for category, tags in self.categories.items():
            dir_path = Path(f'{self.images_store}/{category}')
            existing_files = {file.name for file in dir_path.iterdir()} if dir_path.exists() else set()
            self.downloaded_files[category] = existing_files            
            existing_files_count = len(existing_files)
            self.logger.info(f"{category} has {existing_files_count} files already downloaded.")
            remaining_files_count = max(self.total_photos_limits[category] - existing_files_count, 0)
            if remaining_files_count > 0:
                url = self.get_api_url(tags=tags, page=1)
                yield scrapy.Request(url, callback=self.parse, meta={'category': category, 'page': 1, 'tags': tags, 'remaining_files_count': remaining_files_count})

    def get_api_url(self, tags, page):
        params = {
            'method': 'flickr.photos.search',
            'api_key': self.api_key,
            'tags': tags,
            'tag_mode': 'any',
            'sort': 'relevance',
            'per_page': 500,
            'page': page,
            'content_types': 0,
            'media': 'photos',
            'format': 'json',
            'nojsoncallback': 1,
        }
        return f"https://www.flickr.com/services/rest/?{urlencode(params)}"

    def parse(self, response):
        data = response.json()
        photos = data.get('photos', {}).get('photo', [])
        category = response.meta['category']
        tags = response.meta['tags']
        page = response.meta['page']
        remaining_files_count = response.meta['remaining_files_count']

        if not photos:
            self.logger.info(f"No more photos available for {category}.")
            return

        for photo in photos:
            photo_url = f"https://live.staticflickr.com/{photo['server']}/{photo['id']}_{photo['secret']}_w.jpg"
            filename = photo_url.split('/')[-1]
            if filename not in self.downloaded_files[category]:
                self.downloaded_files[category].add(filename)
                item = FlickrDownloaderItem(file_urls=[photo_url], tag=category)
                yield item
                remaining_files_count -= 1
                if remaining_files_count <= 0:
                    break

        if remaining_files_count > 0:
            next_page = page + 1
            next_page_url = self.get_api_url(tags=tags, page=next_page)
            yield scrapy.Request(next_page_url, callback=self.parse, meta={'category': category, 'page': next_page, 'tags': tags, 'remaining_files_count': remaining_files_count})
