# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request

class TaggedImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for file_url in item['file_urls']:
            yield Request(file_url, meta={'tag': item['tag']})

    def file_path(self, request, response=None, info=None, *, item=None):
        tag = request.meta['tag']
        image_guid = request.url.split('/')[-1]
        return f'{tag}/{image_guid}'
