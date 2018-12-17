# -*- coding: utf-8 -*-

#  Python3爬取楼盘信息，并用机器学习预测房价走向
# （因为个人想了解江城区的房价，所以，以阳江市江城区楼盘房价为例）
# http://yangjiang.newhouse.fang.com/house/s/jiangchengqu/?ctm=1.yangjiang.xf_search.lpsearch_area.2

import requests
from bs4 import BeautifulSoup



url = 'http://yangjiang.newhouse.fang.com/house/s/jiangchengqu/?ctm=1.yangjiang.xf_search.lpsearch_area.2'
response = requests.get(url)  # 获取页面内容
if response.status_code == 200:
    soup = BeautifulSoup(response.text.encode("latin1").decode("gbk"), 'html.parser')  # 先转成latin1编码，再解码为gbk编码。用BeautifulSoup解析
    houses = soup.select(".nhouse_list ul li")  # 选择到房价所在的<ul>标签
    for house in houses:
        try:
            print("https:" + house.select(".nlcd_name a")[0]['href'])
        except Exception as e:
            print("---->", e)
