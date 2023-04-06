import scrapy
from itemloaders.processors import TakeFirst
from scrapy.loader import ItemLoader
from football_clubs.items import FootballClubsItem


class ClubsSpider(scrapy.Spider):
    name = "clubs"
    allowed_domains = ["football.ua"]
    start_urls = ["http://football.ua/"]
    club_id = 0

    def parse(self, response, *kwargs):
        for link in response.css('section.top-teams a::attr(href)'):
            yield response.follow(link, self.parse_club)

    def parse_club(self, response):
        loader = ItemLoader(item=FootballClubsItem(), response=response)
        loader.default_output_processor = TakeFirst()
        self.club_id += 1
        loader.add_value("club_id", self.club_id)
        loader.add_css("club_name", "div.info-intro h1::text")
        loader.add_css("league_name", "article.game-feed.premier-league h3::text")
        loader.add_css("logo_link", "div.info-logo img::attr(src)")
        loader.add_xpath("web_site_link", "//div[@class='info-intro']//td/a[@target]/@href")
        yield loader.load_item()

