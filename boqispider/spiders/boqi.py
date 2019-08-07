# -*- coding: utf-8 -*-
import re
import datetime

from boqispider.items import *

now_time = datetime.date.today()


class BoqiSpider(scrapy.Spider):
    name = 'boqi'
    allowed_domains = ['boqii.com']
    start_urls = ['http://shop.boqii.com/']

    def parse(self, response):
        for a in range(2, 4):
            home_tags = response.xpath('//*[@id="nav"]/div/div[2]/a[' + str(a) + ']').get()
            home_tags_href = re.search('href="(.*?)"', home_tags)
            if home_tags_href:
                home_tags_href_str = home_tags_href.group(1).replace("null", "None")
                yield scrapy.http.Request(url=home_tags_href_str, callback=self.goods_category_self)

    def goods_category_self(self, response):
        goods_category_tags = response.xpath('//*[@id="channel"]/div[2]/a').extract()
        for category in goods_category_tags:
            category_href = re.search('href="(.*?)"', category)
            if category_href:
                category_href_str = category_href.group(1).replace("null", "None")
                yield scrapy.http.Request(url=category_href_str, callback=self.goods_page_self)

    def goods_page_self(self, response):
        page_str = response.xpath('//*[@id="listcontent"]/div[2]/div[2]/div[2]/div[1]/span[1]/text()').get()
        page_int = re.search("共(.*)件", page_str).group(1)
        for n in range(1, int(int(page_int) / 20)):
            category_href_str_cur = str(re.search('(.*?)\.html', response.url).group(1)) + "-p" + str(n) + ".html"
            yield scrapy.http.Request(url=category_href_str_cur, callback=self.goods_list_self)

    def goods_list_self(self, response):
        goods_detail_href = response.xpath('//*[@id="listcontent"]/div[2]/div[3]/div/ul/li/div[2]/a').extract()
        if goods_detail_href:
            for goods_detail_href_one in goods_detail_href:
                goods_detail = re.search('href="(.*?)"', goods_detail_href_one)
                if goods_detail:
                    goods_detail_str = goods_detail.group(1).replace("null", "None")
                    yield scrapy.http.Request(url=goods_detail_str, callback=self.goods_detail_self)

    def goods_detail_self(self, response):
        # 获取商品信息
        # sku
        shop_sku = response.xpath('//*[contains(text(),"商品编号")]/span/text()').get()
        # 商品名称
        shop_name = response.xpath('//*[@id="content"]/div[2]/div[1]/div[2]/div[1]/input[@id="goodname"]').get()
        shop_name_str = re.search('value="(.*?)"', shop_name).group(1)
        # 品牌
        shop_brand = response.xpath('//*[@id="content"]/div[2]/div[1]/div[3]/div[2]/dl[1]/dd/a/text()').get()
        # 商品价格
        shop_price = response.xpath('//*[@id="bqPrice"]/text()').get()
        shop_price_str = re.search('¥(\S*)', shop_price).group(1)
        # 评分
        shop_point = response.xpath('//*[@id="content"]/div[2]/div[1]/div[3]/div[2]/dl[4]/dd/div[1]/em/text()').get()
        shop_point_str = re.search('(.*)分', shop_point).group(1)
        # 规格包装
        shop_ggbz = response.xpath('//*[contains(text(),"商品规格")]/span/text()').get()
        # 销量
        shop_sales_num = response.xpath('//*[@id="content"]/div[2]/div[1]/div[3]/div[2]/dl[3]/dd/text()').get()
        shop_sales_num_str = re.search('(.*)件', shop_sales_num).group(1)
        # 重量
        shop_weight = response.xpath('//*[contains(text(),"重量")]/span/text()').get()
        # 分类
        try:
            shop_category_str1 = response.xpath('//*[@id="content"]/div/div/a[2]/text()').get()
            shop_category_str2 = response.xpath('//*[@id="content"]/div/div/a[3]/text()').get()
            shop_category_str3 = response.xpath('//*[@id="content"]/div/div/a[4]/text()').get()
            shop_category_str = shop_category_str1 + ">" + shop_category_str2 + ">" + shop_category_str3
        except:
            shop_category_str = "无"
        data_list = (now_time, response.url, shop_sku, shop_name_str, shop_brand, shop_price_str, shop_point_str, shop_ggbz, shop_category_str, shop_sales_num_str, shop_weight)
        boqispider_item = BoqispiderItem()
        boqispider_item['data_list'] = data_list
        boqispider_item.save()
