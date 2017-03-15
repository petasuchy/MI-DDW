import scrapy


class BlogSpider(scrapy.Spider):
    name = 'ddw-hw01'
    allowed_domains = ['diit.cz']
    start_urls = ['http://diit.cz/']
    counter = 0;
    parsedCounter = 0;

    def parse(self, response):
        directory = response.url.split("/")[3]
        if directory == "clanek":
            autor = str(response.css('div.author-info h2::text').extract())
            autor = ' '.join(autor.split())
            yield {'title': response.css('title::text').extract(),
                   'author': autor,
                   'date': response.css('div.submitted.content-container > span:nth-child(1)::text').extract(),
                   'text': response.css('div.filtered_html p::text').extract()}
            print("[{}] {}".format(self.counter, response.url))
            self.counter += 1

        links = response.css('a::attr(href)').extract()

        for link in links:
            if link.startswith("/clanek/") and "diskuse" not in link:
                yield scrapy.Request(response.urljoin(link.split("#")[0]), callback=self.parse)
