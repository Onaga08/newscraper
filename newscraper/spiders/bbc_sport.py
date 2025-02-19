import scrapy
import os
from scrapy.selector import Selector
from newscraper.spiders.utils.operations import process_element_data
import json
from newscraper.spiders import BaseSpider

class BBCSpider(BaseSpider):
    name = "bbc_sport_spider"

    def start_requests(self):
        url = "https://bbc.com/sport"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        divs = response.css("div.sc-c6f6255e-0.eGcloy").getall()
        for index, div_html in enumerate(divs):
            div_html = Selector(text=div_html)
            data = process_element_data(div_html, self.selectors, response.meta)

            # Prepare the output file name (e.g., based on the position or any unique identifier)
            file_name = f"item_{index + 1}.txt"
            file_path = os.path.join('scraped_items', file_name)  # Ensure files are saved in a separate directory
            
            # Create the 'scraped_items' directory if it doesn't exist
            if not os.path.exists('scraped_items'):
                os.makedirs('scraped_items')

            # Write the scraped data to the .txt file
            with open(file_path, 'w', encoding='utf-8') as f:
                # Write the data as a string (you can format it as needed)
                f.write(json.dumps(data, ensure_ascii=False, indent=4))

            yield {
                "position": index + 1,
                **data
            }
