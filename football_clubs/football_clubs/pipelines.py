# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
from football_clubs.models import db_connect, create_table, FootballClubsData, PlayersData
from sqlalchemy.orm import sessionmaker
import pandas as pd
from itemadapter import ItemAdapter


class FileCsvPipeline:

    def __init__(self):
        self.data = pd.DataFrame()

    def process_item(self, item, spider):
        main_data = ItemAdapter(item).asdict()
        df = pd.DataFrame.from_records([main_data])
        self.data = pd.concat([self.data, df], ignore_index=True)

        return item

    def close_spider(self, spider):
        self.data.to_csv(f'{spider.name}.csv', index=False)


class FileJsonPipeline:

    def open_spider(self, spider):
        self.file = open(f'{spider.name}.jsonl', 'w', encoding='utf-8')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict(), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item


class SqlalchemyPipeline(object):
    def __init__(self):
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        if spider.name == 'clubs':
            self.process_item_clubs(item, spider)
            return item
        elif spider.name == 'players':
            self.process_item_players(item, spider)
            return item
        else:
            raise

    def process_item_clubs(self, item, spider):
        session = self.Session()
        fc_table = FootballClubsData()
        fc_table.club_name = item["club_name"]
        fc_table.logo_link = item['logo_link']
        fc_table.league_name = item["league_name"]
        fc_table.web_site_link = item["web_site_link"]

        try:
            session.add(fc_table)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def process_item_players(self, item, spider):
        session = self.Session()
        pl = PlayersData()
        pl.name = item['name']
        pl.club = item['club']
        pl.position = item['position']
        pl.birthday = item.get('birthday')
        pl.motherland = item['motherland']
        pl.photo_link = item.get('photo_link')

        try:
            session.add(pl)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
