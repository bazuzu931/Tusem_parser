
import scrapy
import os
from time import sleep


BASE_DIR  = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TusemSpiderSpider(scrapy.Spider):

	name = 'tusem-spider'
	# allowed_domains = ['http://www.tusvideolari.com/']
	start_urls = ['http://www.tusvideolari.com']

	def parse(self, response):

		urls = response.css('ul.sub-menu > li.menu-item > a::attr(href)').extract()

		for url in urls:


			yield  scrapy.Request(url=url, callback=self.each_page)




	def each_page(self, response):

		tus_folder = response.css('header.entry-header > h1::text').extract_first()
		if not os.path.exists(BASE_DIR + '/list/' + tus_folder):
			os.makedirs(BASE_DIR + '/list/' + tus_folder)

		page_urls = response.css('.video-thumbimg > a::attr(href)').extract()
		for page_url in page_urls:
			yield   scrapy.Request(url=page_url, callback=self.each_link, meta={'folder_name':tus_folder} )
			



	def each_link(self, response):

		res = response.css('#player > iframe::attr(src)').extract_first() + '\n'

		tus_folder = response.meta['folder_name']
		tus_folder_path = BASE_DIR + '/list/' + tus_folder
		tus_file_name = tus_folder + '.txt'
		tus_file = tus_folder_path + tus_file_name

		if not os.path.exists(tus_file):
			with open(tus_file, 'w') as f:
				f.write(res)
		else:
			with open(tus_file, 'a') as f:
				f.write(res)

		command = "youtube-dl --output '" + tus_folder_path + "/%(title)s.%(ext)s' -c " + str(res)
		os.system(command)
		sleep(1)