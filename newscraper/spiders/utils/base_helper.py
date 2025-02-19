


def extract_detailed_data(self, response):
    """
    Function to extract detailed data from a given page.
    You will need to define how to scrape the detailed information from the page.
    """
    detailed_data = {}

    title = response.xpath('//h1[@class="sc-518485e5-0 bWszMR"]/text()').get()
    if title:
        detailed_data['title'] = title.strip()
    detailed_data['author'] = response.xpath('//span[contains(@class, "sc-b42e7a8f-7 khDNZq")]/text()').get()
    detailed_data['content'] = ' '.join(response.xpath('//div[contains(@class, "sc-18fde0d6-0")]//p/text()').getall())
    if len(detailed_data['content']) < 5:
        print("its empty")
        detailed_data['content'] = ' '.join(response.xpath('//div[contains(@class, "sc-b7984e68-3 hoGYFg")]//p/text()').getall())
        print(f"detailed_data ----> {detailed_data}")

    return detailed_data