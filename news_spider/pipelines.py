# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


# class NewsSpiderPipeline(object):
#     def process_item(self, item, spider):
#         return item
from scrapy.exporters import CsvItemExporter


class CsvPipeline(object):  # modify items_pipeline in settings.py to invoke pipelining

    def __init__(self):
        self.file = open("data.csv", 'wb')          # open csv file in wb = writing + binary mode
        self.exporter = CsvItemExporter(self.file)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    # def create_valid_csv(self, item):
    #     for key, value in item.items():
    #         is_string = (isinstance(value, basestring))
    #         if (is_string and ("," in value.encode('utf-8'))):
    #             item[key] = "\"" + value + "\""
