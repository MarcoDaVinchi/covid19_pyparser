import scrapy


class CovidSpider(scrapy.Spider):
    name = "covid"

    start_urls = ['https://multimedia.scmp.com/widgets/china/wuhanvirus/']

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = "%s.html" % page
        with open(filename, "wb") as f:
            f.write(response.body)
        self.log("Saved file %s" % filename)
