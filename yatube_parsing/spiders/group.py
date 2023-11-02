import scrapy


class GroupSpider(scrapy.Spider):
    name = "group"
    allowed_domains = ["51.250.32.185"]
    start_urls = ["http://51.250.32.185/"]

    def parse(self, response):
        all_groups = response.css('a[href^="/group/"]')
        for author_link in all_groups:
            yield response.follow(author_link, callback=self.parse_group)

        # Переход по страницам пагинации (точно как в пауке quotes).
        next_page = response.xpath("//a[contains(., 'Следующая')]/@href").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_group(self, response):
        yield {
            'group_name': response.css('h2::text').get(),
            'description': response.css('p.group_descr::text').get(),
            'posts_count': int(response.css('div.h6.text-muted.posts_count::text').get().strip().replace('Записей: ', ''))
        }
