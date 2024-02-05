# Flickr Scraper

A Scrapy-based Flickr API scraper to download images based on user-defined categories and tags. Ideal for creating categorized image datasets.

## Features

- Downloads images across multiple user-defined categories.
- Allows setting unique tags and image limits for each category.

## Setup

### Requirements

- Python 3.6 or higher
- Scrapy

### Installation

Clone the repository and install Scrapy:

```bash
git clone https://github.com/deepinvalue/flickr-scraper.git
cd flickr-scraper
pip install scrapy
```

### Configuration

1. Rename `config.sample.json` to `config.json`.
2. Edit `config.json` with your Flickr API key, specify the images storage path, and detail each category with its tags and image limits.

## Usage

```bash
scrapy crawl flickr
```