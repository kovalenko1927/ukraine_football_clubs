import scrapy
from itemloaders.processors import TakeFirst
from scrapy.loader import ItemLoader

from football_clubs.items import FootballPlayersItem


class PlayersSpider(scrapy.Spider):
    name = "players"
    allowed_domains = ["football.ua"]
    start_urls = ["http://football.ua/"]
    player_id = 0

    def parse(self, response, *kwargs):
        for link in response.css('section.top-teams a::attr(href)'):
            yield response.follow(link, self.parse_club)

    def parse_club(self, response):
        for link in response.css('article.team-consist a::attr(href)'):
            yield response.follow(link, self.parse_player)

    def parse_player(self, response):
        loader = ItemLoader(item=FootballPlayersItem(), response=response)
        loader.default_output_processor = TakeFirst()
        self.player_id += 1
        loader.add_value("player_id", self.player_id)
        loader.add_css("name", "div.info-intro h1::text")
        loader.add_xpath("club", "//tr/td[contains(text(), 'Клуб')]/following-sibling::td/a/text()")
        loader.add_xpath("position", "//tr/td[contains(text(), 'Амплуа')]/following-sibling::td/text()")
        loader.add_xpath("birthday", "//tr/td[contains(text(), 'Дата рождения')]/following-sibling::td/text()")
        loader.add_xpath("motherland", "//tr/td[contains(text(), 'Гражданство')]/following-sibling::td/text()")
        loader.add_css("photo_link", "div.info-logo img::attr(src)")
        yield loader.load_item()
