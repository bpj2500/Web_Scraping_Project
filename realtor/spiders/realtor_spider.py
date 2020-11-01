#realtor spider bot 

from scrapy import Spider, Request  
from realtor.items import RealtorItem 

class RealtorSpider(Spider): 
    name = 'realtor_spider' 
    allowed_urls = ['www.realtor.com'] 
    start_urls = ['https://www.realtor.com/realestateandhomes-search/Manhattan_NY'] 

    def parse(self, response): 
    #gives the final page number on the site 
    #the page urls have a similar format with the exception of the page number
    
        #num_pages = int(response.xpath('//div[@class="jsx-4039137973 pagination-wrapper text-center"]/ul/li[@class="jsx-4098248002 pagination-number pagination-exceeds-srp-max"]/text()').extract_first())
    
        #Formatting the urls
        url_list = [f'https://www.realtor.com/realestateandhomes-search/Manhattan_NY/pg-{i}' for i in range(70, 91)]  

        #for url in url_list[:5]: #check to see if xpath worked, it did!
            #print('=' * 50)
            #print(url) 
            #print('=' * 50) 
        for url in url_list:  

            yield Request(url=url, callback=self.parse_web_page) 


    def parse_web_page(self, response):  
        # print("hooray")

        listing_page_urls = response.xpath('//div[@data-testid="property-detail"]/a/@href').extract()
        #print(len(listing_page_urls))

        domain, _ = response.url.split('/r') 

        listing_urls = [domain + refer for refer in listing_page_urls]

        for listing in listing_urls:
            # print("=" * 50)
            # print(listing)

            yield Request(url=listing, callback=self.parse_list_page)


    def parse_list_page(self, response):  

        #print("=" * 50)
        #print(response.url)
        #print(price)
 
        price = response.xpath('//div[@class="jsx-1959108432 price-section"]/span/text()').extract_first() 
        num_beds = response.xpath('//div[@data-testid="listing-information-cmp"]/div[@data-testid="property-meta-container"]/ul/li[@data-label="pc-meta-beds"]/span[@data-label="meta-value"]/text()').extract_first()
        have_beds = response.xpath('//div[@data-testid="listing-information-cmp"]/div[@data-testid="property-meta-container"]/ul/li[@data-label="pc-meta-beds"]/span[@data-label="meta-label"]/text()').extract_first()
        num_baths = response.xpath('//div[@data-testid="listing-information-cmp"]/div[@data-testid="property-meta-container"]/ul/li[@data-label="pc-meta-baths"]/span[@data-label="meta-value"]/text()').extract_first()
        area = response.xpath('//div[@data-testid="address-section"]/h1/span/text()').extract_first() 
        sqft = response.xpath('//div[@data-testid="property-meta-container"]/ul/li[@data-label="pc-meta-sqft"]/span[@data-label="meta-value"]/text()').extract_first()
        
        attribute_dict = {}
        rows = response.xpath('//li[@class="jsx-488154125 col-xs-6 col-md-4 indicator"]')

        for row in rows:
            key = row.xpath('./div/span[1]/text()').extract_first()
            value = row.xpath('./div/span[2]/text()').extract_first()
            attribute_dict[key] = value

        property_type = attribute_dict.get('Property Type')
        year_built = attribute_dict.get('Year Built')
        
        item = RealtorItem() 
        item['price'] = price 
        item['beds'] = num_beds 
        item['baths'] = num_baths 
        item['sqft'] = sqft 
        item['property_type'] = property_type 
        item['area'] = area  
        item['have_beds'] = have_beds
        item['year_built'] = year_built


        yield item 
#must revise the way the items are collected, perhaps split the items up
        



