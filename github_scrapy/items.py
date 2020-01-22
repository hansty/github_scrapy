# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GithubScrapyItem(scrapy.Item):
	issue = scrapy.Field()
	issueHref = scrapy.Field()
	repoName = scrapy.Field()
	repoOwner = scrapy.Field()
	repoHref = scrapy.Field()
	dateOpened = scrapy.Field()
	issueId = scrapy.Field()
	issueStatus = scrapy.Field()
	linesChanged = scrapy.Field()
	filesChanged = scrapy.Field()
	checks = scrapy.Field()
	commits = scrapy.Field()
	comments = scrapy.Field()
	repoTags = scrapy.Field()
	repoInfo = scrapy.Field()
	repoCommits = scrapy.Field()
	repoWatchers = scrapy.Field()
	repoStargazers = scrapy.Field()
	repoForks = scrapy.Field()
	dateLastComment = scrapy.Field()
    # define the fields for your item here like:
    # name = scrapy.Field()

