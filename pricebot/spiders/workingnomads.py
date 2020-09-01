import scrapy
from itemadapter import ItemAdapter
from pricebot.items import Job
import json

class WorkingNomadsSpider(scrapy.Spider):
    name = "workingnomads"
    start_urls = ["https://www.workingnomads.co/api/exposed_jobs/"]

    def parse(self, response):
        jsonresponse = json.loads(response.body)
        for job_item in jsonresponse:
            if job_item['location'] not in ['North America', 'USA']:
                job = Job()
                job['position'] = job_item['title']
                job['company'] = job_item['company_name']
                job['url'] = job_item['url']

                yield ItemAdapter(job).asdict()