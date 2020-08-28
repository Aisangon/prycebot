import scrapy
from itemadapter import ItemAdapter
from pricebot.items import Job
from urllib.parse import urljoin

class RemotiveSpider(scrapy.Spider):
    name = "remotive"
    start_urls = ["https://remotive.io/remote-jobs/software-dev"]
    base_url = "https://remotive.io/"

    def parse(self, response):
        for job_item in response.css('li.job-list-item'):
            job = Job()
            job['position'] = job_item.css('.position a::text').get()
            job['company'] = job_item.css('.company span::text').get()
            job['url'] = urljoin(self.base_url, job_item.css('.position a::attr(href)').get())

            yield ItemAdapter(job).asdict()
