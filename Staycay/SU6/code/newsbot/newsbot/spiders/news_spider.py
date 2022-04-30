import scrapy
import requests


class NewsItem(scrapy.Item):
    source = scrapy.Field()
    title = scrapy.Field()
    text = scrapy.Field()
    url = scrapy.Field()


class NewsSpider(scrapy.Spider):
    name = 'news'
    allowed_domains = ['sg.news.yahoo.com']
    start_urls = ['https://sg.news.yahoo.com']

    def parse(self, response):
        lis = response.xpath('//*[@id="YDC-Stream"]/ul/li')
        items = []
        list_number = 1
        for li in lis:
            print('News ID: ', list_number)
            list_number = list_number + 1
            src = li.xpath('//*[@id="YDC-Stream"]/ul/li[' + str(list_number) +
                           ']/div/div/div[2]/div[2]/text()').extract()
            news_url = li.xpath('//*[@id="YDC-Stream"]/ul/li[' + str(list_number) +
                                ']/div/div/div[2]/h3/a/@href').extract()
            news_title = li.xpath('//*[@id="YDC-Stream"]/ul/li[' + str(list_number) +
                                  ']/div/div/div[2]/h3/a//text()').extract()
            if src and news_url:
                request = requests.get(self.start_urls[0] + news_url[0])
                # as the file is large, I only keep part of the text.
                # of course you can also scrap and store the full text
                text = request.text[-5100:-5000]
                items.append(NewsItem(source=src[0], title=news_title[0], url=news_url[0], text=text))
        return items
