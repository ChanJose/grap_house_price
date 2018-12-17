# -*- coding: utf-8 -*-

#  Python3爬取楼盘信息，并用机器学习预测房价走向
# （因为个人想了解江城区的房价，所以，以阳江市江城区楼盘房价为例）
# http://yangjiang.newhouse.fang.com/house/s/jiangchengqu/?ctm=1.yangjiang.xf_search.lpsearch_area.2
# 在grap_house_price2.py原基础上，进行封装

import requests
from bs4 import BeautifulSoup

# 获取各个楼盘的原页面链接
def get_houses_urls(origin_url):
    response = requests.get(origin_url)  # 获取页面内容
    if response.status_code == 200:
        soup = BeautifulSoup(response.text.encode("latin1").decode("gbk"),
                             'html.parser')  # 先转成latin1编码，再解码为gbk编码。用BeautifulSoup解析
        houses = soup.select(".nhouse_list ul li")  # 选择到房价所在的<ul>标签
        houses_urls = []  # 楼盘原页面链接
        for house in houses:
            try:
                houses_urls.append("https:" + house.select(".nlcd_name a")[0]['href'])

            except Exception as e:  # 如果出错，返回空
                print(e)  # 打印出错原因
        return houses_urls


if __name__ == "__main__":
    origin_url = 'http://yangjiang.newhouse.fang.com/house/s/jiangchengqu/?ctm=1.yangjiang.xf_search.lpsearch_area.2'  # 阳江江城区楼盘链接
    urls = get_houses_urls(origin_url)  # 获取上述链接对应的页面中所有楼盘的原页面链接
    print(len(urls))
    if len(urls) > 0:
        print(urls)
