from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request
import scrapy.log

import datetime
import json


class BaseJobsSpider(CrawlSpider):

	def scrape_html(self, response, f):
		entry={'URL':response.url, 'HTML':response.body}
		json.dump(entry, f)
		f.write("\n")
		f.close()

	def scrape_summary(self, response):
		f = open(self.fpath, 'a')
		self.scrape_html(response, f)

	def scrape_details(self, response):
		f = open(self.fpath_detail, 'a')
		self.scrape_html(response, f)
	
class JobsSpiderRu(BaseJobsSpider):

	# Identify the spider
	country = "Russia"
	name = country + "_spider"
	allowed_domains = ['jobs.ru']
	start_urls = ['http://www.jobs.ru']

	# Rules for which links to follow
	rule1 = Rule(SgmlLinkExtractor(allow='/vacancy/region/'), 
				callback='scrape_summary',follow=True)
	rule2 = Rule(SgmlLinkExtractor(allow='/vacancy/view/'), 
				callback='scrape_details',follow=False)

	rules = (rule1, rule2,)
	#rules = (rule1,)

	# Output results
	folder = 'scraped_data/Russia/' 
	time_stamp = str(datetime.datetime.now())
	fname = country + "_" + time_stamp
	fpath = folder + fname + '.json'
	fpath_detail = folder + fname + '_detail.json'

	# Logging. Create a log file
	logfile = open(folder + fname + ".log", 'w')
	log_observer = scrapy.log.ScrapyFileLogObserver(logfile, level = scrapy.log.INFO)
	log_observer.start()

class Jobs_bg_Spider(BaseJobsSpider):
	country = "Bulgaria"
	name = country + "_spider"
	allowed_domains = ['jobs.bg']
	start_urls = ['http://www.jobs.bg/front_job_search.php']
	rule1 = Rule(SgmlLinkExtractor(allow='front_job_search\.php\?'), 
						callback='scrape_summary',follow=True)
	rules = (rule1,	)

	folder = 'scraped_data/Bulgaria/' 
	time_stamp = str(datetime.datetime.now())
	fname = country + "_" + time_stamp
	fpath = folder + fname + '.json'
	fpath_detail = folder + fname + '_detail.json'

	# Logging. Create a log file
	logfile = open(folder + fname + ".log", 'w')
	log_observer = scrapy.log.ScrapyFileLogObserver(logfile, level = scrapy.log.INFO)
	log_observer.start()

