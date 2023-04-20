# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json

from football_clubs.models import DBClient

from itemadapter import ItemAdapter

import pandas as pd


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


class DBPipeline:
    def open_spider(self, spider):
        self.client = DBClient(table_name=spider.name)

    def process_item(self, item, spider):
        self.client.save_data([item])
        return item
