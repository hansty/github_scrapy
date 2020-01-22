# -*- coding: utf-8 -*-
import scrapy
from ..items import GithubScrapyItem

class TensorflowSpiderSpider(scrapy.Spider):
    name = 'tensorflow_spider_old'
    allowed_domains = ['github.com']
    start_urls = ['https://github.com/search?q=tensorflow+created%3A2019-09-21&type=Issues']

    
    def parse(self, response):

        item = GithubScrapyItem()
        issueDivs = response.css('div.issue-list-item')
        for div in issueDivs:

            item['issue'] = div.css('h3 a::attr(title)').extract()
            item['issueId'] = div.css('span.text-gray::text').extract()
            item['dateOpened'] = div.css('relative-time::attr(datetime)').extract()

            item['issueHref'] = div.css('h3 a::attr(href)').get()
            
            yield item