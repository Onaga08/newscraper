import scrapy
import os
import json

class BaseSpider(scrapy.Spider):  # Make sure the class name is capitalized
    def __init__(self, *args, **kwargs):
        super(BaseSpider, self).__init__(*args, **kwargs)  # Fixed reference to the class

        # Get the absolute path to the current file's directory
        home = os.path.dirname(os.path.abspath(__file__))        
        selectors_path = os.path.join(home, 'selectors.json')  # Use os.path.join for cross-platform compatibility
        
        # Load the selectors.json configuration
        with open(selectors_path, 'r') as f:
            self.config = json.load(f)

        spider_name = self.name  # Get the name of the spider
        if spider_name in self.config:
            self.selectors = self.config[spider_name]
        else:
            self.selectors = {}  # Default to an empty dict or raise an error if you prefer
            self.logger.warning(f"No selectors found for spider {spider_name}")
            
        os.makedirs('scraped_items', exist_ok=True)
