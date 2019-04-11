import scrapy
from items import ExtractnewsarticlesItem


class Scapper(scrapy.Spider):
    name = 'news'
    start_urls = ['https://www.reuters.com']
    address_list = []

    def parse(self, response):
        market_section = response.css('li#nav-item-3')
        nav_links = market_section.css('a::attr(href)').extract()
        for link in nav_links:
            if link.startswith('/'):
                nav_url = response.urljoin(link)
                print('URL = ' + nav_url)
                yield scrapy.Request(nav_url, callback=self.parse_navbar_content, dont_filter=True)

    def parse_navbar_content(self, response):
        news_section = response.css('section.module-content')
        section_url = news_section.css('a::attr(href)').extract()
        for url in section_url:
            domain_url = response.urljoin(url)
            if url.startswith('/article'):
                yield scrapy.Request(domain_url, callback=self.parse_article, dont_filter=True)
            #else:
                #yield scrapy.Request(domain_url, callback=self.parse_navbar_content, dont_filter=True)

    def parse_article(self, response):
        address = response.request.url
        if address not in self.address_list:
            self.address_list.append(address)
            item = ExtractnewsarticlesItem()
            item['address'] = address
            item['title'] = response.css('h1.ArticleHeader_headline::text').extract()
            article = response.css('div.StandardArticleBody_body > p::text').extract()
            item['content'] = "".join(str(data) for data in article).encode('utf8')
            yield item

