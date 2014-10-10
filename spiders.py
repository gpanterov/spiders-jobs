from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request

class JobsSpider(CrawlSpider):
	name="jobs_bg_spider"
	allowed_domains = ['jobs.bg']
	start_urls = ['http://www.jobs.bg/front_job_search.php?first=1&str_regions=&str_locations=&tab=jobs&old_country=26&country=26&region=0&l_category%5B%5D=0&keyword=']

	rules = (
	Rule(SgmlLinkExtractor(allow='front_job_search\.php\?'), callback='parse_jobs',follow=True),
	)

	def parse_jobs(self, response):
		hxs = HtmlXPathSelector(response)
		# Scrape name and web addresses of company
		dates = hxs.select("//table//td[@width=60]/text()").extract()
		titles = hxs.select("//table//td[@width=280]//a[@class='MainLinkBold']/text()").extract()
		companies = hxs.select("//table//td[@width=130]//a[@class='company_link']/text()").extract()
		dates = dates[1:]
		f = open('jobs.csv', 'a')
		for i in range(len(dates)):
			try:
				f.write(dates[i].encode('utf8') + ',')
				f.write(titles[i].encode('utf8') + ',')
				f.write(companies[i].encode('utf8') + '\n')
			except:
				pass
		f.close()

