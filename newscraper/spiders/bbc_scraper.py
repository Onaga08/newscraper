import scrapy
import os
from scrapy.selector import Selector
from newscraper.spiders.utils.operations import process_element_data
from newscraper.spiders.utils.base_helper import extract_detailed_data
import json
from newscraper.spiders import BaseSpider

class BBCSpider(BaseSpider):
    name = "bbc_spider"

    def start_requests(self):
        url = "https://www.bbc.com/"
        yield scrapy.Request(
            url=url, 
            callback=self.parse
            )

    def parse(self, response):
        divs = response.css("div.sc-c6f6255e-0.eGcloy").getall()
        for index, div_html in enumerate(divs):
            div_html = Selector(text=div_html)
            data = process_element_data(div_html, self.selectors, response.meta)
            
            # Yield data to CSV (for the headlines and initial data)
            yield {
                "position": index + 1,
                **data
            }
            
            # After yielding to CSV, make further requests for detailed scraping
            next_url = data["url"]
            if next_url:
                yield scrapy.Request(next_url, 
                                    callback=self.parse_detailed_page, 
                                    meta={
                                        'position': index + 1, 
                                        'initial_data': data
                                        }
                                    )

    def parse_detailed_page(self, response):
        detailed_data = extract_detailed_data(response)
        initial_data = response.meta['initial_data']   
        combined_data = {**initial_data, **detailed_data}
        
        file_name = f"item_{response.meta['position']}_detailed.json"
        file_path = os.path.join('scraped_items', file_name)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(combined_data, ensure_ascii=False, indent=4))
        
        yield combined_data
