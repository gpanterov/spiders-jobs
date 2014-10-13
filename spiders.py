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

class JobsSpiderRu(CrawlSpider):
	name="jobs_ru_spider"
	allowed_domains = ['jobs.ru']
	start_urls = ['http://www.jobs.ru/vacancy/region/%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0/1/0']

	rules = (
	Rule(SgmlLinkExtractor(allow='/region/%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0/1'), callback='parse_jobs',follow=True),
	)

	def parse_jobs(self, response):
		hxs = HtmlXPathSelector(response)
		# Scrape name and web addresses of company
		titles = hxs.select("//div[@class='listrow']/a/text()").extract()
		posting_text = hxs.select("//div[@class='listrow']/span[@class='listtext']/text()").extract()
		posting_date = hxs.select("//div[@class='listrow']/span[@class='listdate']/text()").extract()
		f = open('jobs_ru.csv', 'a')
		for i in range(len(titles)):
			f.write(titles[i].encode('utf8') + ';')
			f.write(posting_text[i].encode('utf8') + ';')
			f.write(posting_date[i].encode('utf8') + '\n')

		f.close()

