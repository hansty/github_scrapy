# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.request import Request
from ..items import GithubScrapyItem

class TensorflowSpiderV2Spider(scrapy.Spider):
    name = 'tensorflow_spider'
    allowed_domains = ['github.com']
    start_urls = ['https://github.com/search?p=1&q=tensorflow+created%3A2019-10&type=Issues']
     # start_urls = ['http://www.a.com/%d_%d_%d' %(n,n+1,n+2) for n in range(0, 26)]
    # start_urls = ['https://github.com/search?o=desc&q=tensorflow+created%3A2019-09-21&s=comments&type=Issues']

    def start_requests(self):
        urls = []

        for i in range(1,2):
            urls.append('https://github.com/search?p={0}&q=tensorflow+created%3A2019-10&type=Issues'.format(i))

        for url in urls:
              yield Request(url, self.parse)

    def parse(self, response):
        issues = response.css('h3 a::attr(href)').extract()
        
        for i in issues:
            url = response.urljoin(i)
            request = scrapy.Request(url, callback=self.parse_issue)
            request.meta['issueHref'] = url
            yield request

        # next_page = response.css('div.pagination a.next_page::attr(href)').get()
        # print (next_page)
        # if(next_page is not None):
        #     yield response.follow(next_page, callback=self.parse)

        # next_page = 'https://github.com/search?p='+str(TensorflowSpiderV2Spider.page_number)+'&q=tensorflow+created%3A2019-09-21&type=Issues'
        # print (next_page)
        # if(TensorflowSpiderV2Spider.page_number < 21):
        #     TensorflowSpiderV2Spider.page_number += 1
        #     yield response.follow(next_page, callback=self.parse)

    def parse_issue(self, response):
        item = GithubScrapyItem()
        item['issue'] = response.css('h1.gh-header-title span.js-issue-title::text').extract_first()
        item['issueHref'] = response.meta['issueHref']
        item['repoName'] = response.css('h1.public strong a::text').extract_first()
        item['repoOwner'] = response.css('h1.public span.author a::text').extract_first()
        item['repoHref'] = response.urljoin(response.css('h1.public strong a::attr(href)').extract_first())
        item['issueId'] = response.css('h1.gh-header-title span.gh-header-number::text').extract_first()
        item['issueStatus'] = response.css('span.State::attr(title)').extract_first()
        item['linesChanged'] = response.css('span.diffstat span.tooltipped::attr(aria-label)').extract_first()
        item['filesChanged'] = response.css('nav.tabnav-tabs span#files_tab_counter::text').extract_first()
        item['checks'] = response.css('nav.tabnav-tabs span#commits_tab_counter::text').extract_first()
        item['commits'] = response.css('nav.tabnav-tabs span#conversation_tab_counter::text').extract_first()
        item['comments'] = response.css('nav.tabnav-tabs span#files_tab_counter::text').extract_first()
        item['dateOpened'] = response.css('h3.timeline-comment-header-text relative-time::attr(datetime)').extract_first()
        item['dateLastComment'] = response.css('div.TimelineItem:last-of-type relative-time::attr(datetime)').extract_first()

        request = scrapy.Request(item['repoHref'], callback=self.parse_repo)
        request.meta['item'] = item
        yield request

    def parse_repo(self, response):
        item = response.meta['item']
        item['repoTags'] = response.css('a.topic-tag::attr(title)').extract()
        item['repoInfo'] = response.css('div.f4 span.text-gray-dark::text').extract_first()
        item['repoCommits'] = response.css('li.commits span.num::text').extract_first()
        item['repoForks'] = response.css('ul.pagehead-actions li:last-of-type a.social-count::text').extract_first()
        item['repoStargazers'] = response.css('ul.pagehead-actions li:nth-last-of-type(2) a.social-count::text').extract_first()
        item['repoWatchers'] = response.css('ul.pagehead-actions li:nth-last-of-type(3) a.social-count::text').extract_first()
        yield item