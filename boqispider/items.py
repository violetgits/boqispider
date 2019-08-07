# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import pymysql

connection = pymysql.connect(host='192.168.1.142',
                             user='root',
                             password='erp-888888',
                             db='petgoodsdb',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


class BoqispiderItem(scrapy.Item):
    data_list = scrapy.Field()

    def save(self):
        with connection.cursor() as cursor:
            print(self.get("data_list"))
            sql = "INSERT INTO `boqi_goods` (`busi_date`, `data_source`, `sku`, `name`, `brand`, `price`, `point`, `ggbz`, `category`, `sales_num`, `weight`) " \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, self.get("data_list"))
            connection.commit()
        pass
