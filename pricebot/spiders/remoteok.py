import scrapy
from itemadapter import ItemAdapter
from pricebot.items import Job
from urllib.parse import urljoin

class RemoteOkSpider(scrapy.Spider):
    name = "remoteok"
    start_urls = ["https://remoteok.io/remote-dev-jobs"]
    base_url = "https://remoteok.io/"

    def parse(self, response):
        for job_item in response.css('tr.job.new'):
            job = Job()
            job['position'] = job_item.css('.company_and_position h2::text').get()
            job['company'] = job_item.css('.company_and_position a.companyLink h3::text').get()
            job['url'] = urljoin(self.base_url, job_item.css('td.source a::attr(href)').get())

            yield ItemAdapter(job).asdict()
