from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request
import datetime



class JobsSpider(CrawlSpider):
	country = "Bulgaria"
	name = country + "_spider"
	allowed_domains = ['jobs.bg']
	start_urls = ['http://www.jobs.bg/front_job_search.php?first=1&str_regions=&str_locations=&tab=jobs&old_country=26&country=26&region=0&l_category%5B%5D=0&keyword=']

	rules = (
	Rule(SgmlLinkExtractor(allow='front_job_search\.php\?'), callback='parse_jobs',follow=True),
	)

	folder = 'scraped_data/' 
	time_stamp = str(datetime.datetime.now())
	fname = country + "_" + time_stamp
	fpath = folder + fname
	# Open file for appending and close it to erase any previous data
	f = open(fpath, 'w')
	f.close()
	def parse_jobs(self, response):
		hxs = HtmlXPathSelector(response)
		# Scrape name and web addresses of company
		dates = hxs.select("//table//td[@width=60]/text()").extract()
		titles = hxs.select("//table//td[@width=280]//a[@class='MainLinkBold']/text()").extract()
		companies = hxs.select("//table//td[@width=130]//a[@class='company_link']/text()").extract()
		dates = dates[1:]
		print titles
		for i in range(len(dates)):

			self.write2file(dates[i], titles[i], companies[i])

	def write2file(self, date, title, company):

		f = open(self.fpath, 'a')
		try:

			f.write(date.encode('utf8') + ',')
			f.write(title.encode('utf8') + ',')
			f.write(company.encode('utf8') + '\n')
		except:
			pass
		f.close()


class JobsSpiderRu(CrawlSpider):
	country = "Russia"
	name = country + "_spider"
	allowed_domains = ['jobs.ru']
	start_urls = ['http://www.jobs.ru/vacancy/region/%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0/1/0']

	rules = (
	Rule(SgmlLinkExtractor(allow='/region/%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0/1'), callback='parse_jobs',follow=True),
	)

	folder = 'scraped_data/' 
	time_stamp = str(datetime.datetime.now())
	fname = country + "_" + time_stamp
	fpath = folder + fname
	# Open file for appending and close it to erase any previous data
	f = open(fpath, 'w')
	f.close()

	def parse_jobs(self, response):
		hxs = HtmlXPathSelector(response)
		# Scrape name and web addresses of company
		titles = hxs.select("//div[@class='listrow']/a/text()").extract()
		posting_text = hxs.select("//div[@class='listrow']/span[@class='listtext']/text()").extract()
		posting_date = hxs.select("//div[@class='listrow']/span[@class='listdate']/text()").extract()
		for i in range(len(titles)):
			self.write2file(posting_date[i], titles[i], posting_text[i])

	def write2file(self, date, title, company):

		f = open(self.fpath, 'a')

		f.write(date.encode('utf8') + ',')
		f.write(title.encode('utf8') + ',')
		f.write(company.encode('utf8') + '\n')
		f.close()


