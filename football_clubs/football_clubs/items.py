# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose


class FootballClubsItem(scrapy.Item):
    club_id = scrapy.Field()
    club_name = scrapy.Field()
    league_name = scrapy.Field()
    logo_link = scrapy.Field()
    web_site_link = scrapy.Field()


class FootballPlayersItem(scrapy.Item):
    player_id = scrapy.Field()
    name = scrapy.Field()
    club = scrapy.Field()
    position = scrapy.Field()
    birthday = scrapy.Field()
    motherland = scrapy.Field(input_processor=MapCompose(str.strip))
    photo_link = scrapy.Field()
