# -*- coding: utf-8 -*-

#  Python3爬取楼盘信息，并用机器学习预测房价走向
# （因为个人想了解江城区的房价，所以，以阳江市江城区楼盘房价为例）
# http://yangjiang.newhouse.fang.com/house/s/jiangchengqu/?ctm=1.yangjiang.xf_search.lpsearch_area.2
# 在grap_house_price2.py原基础上，进行封装
# 把最后的结果存到MongoDB中

import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import pymongo  # 导入mongodb的管理库


# 获取各个楼盘的原页面链接
def get_houses_urls(origin_url):
    headers = {
        'User-Agent': 'Mozilla/5.0(Macintosh;Intel Mac OS X 10_12_6) AppleWebKit/537.36(KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    }
    response = requests.get(origin_url, headers=headers)  # 获取页面内容
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
    return None


def get_house_info(url):
    houses_content = {}
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0(Macintosh;Intel Mac OS X 10_12_6) AppleWebKit/537.36(KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
        }
        response = requests.get(url, headers=headers)  # 获取该楼盘页面内容
        if response.status_code == 200:
            soup = BeautifulSoup(response.text.encode("latin1").decode("gbk"),
                                 'html.parser')  # 先转成latin1编码，再解码为gbk编码。用BeautifulSoup解析

            information = soup.select(".information")[0]  # 先选择到关于楼盘信息的<div>,结果是列表，用[0]
            houses_content['楼盘名'] = information.select("h1 strong")[0].text  # 楼盘名
            houses_content['评分'] = information.select(".tit a")[0].text  # 评分
            houses_content['价格'] = information.select(".information_li .prib")[0].text  # 均价
            zlhx_a = information.select(".information_li .zlhx a")  # 主力户型所对应的<a>标签
            zlhx_text = []
            for item in zlhx_a:
                if item.text.strip() != "":
                    zlhx_text.append(item.text.strip())
            houses_content['主力户型'] = (',').join(zlhx_text)  # 主力户型
            houses_content['项目地址'] = information.select("#xfptxq_B04_12 span")[0].text  # 楼盘地址
            kaipan_a = information.select(".information_li .kaipan")
            if len(kaipan_a) > 0:
                houses_content['开盘时间'] = kaipan_a[0].text  # 开盘时间
            else:
                houses_content['开盘时间'] = "暂无"
            return houses_content
        return None
    except RequestException:
        return None


MONGO_URL = 'localhost'  # 或者是:MONGO_URL = '127.0.0.1'
MONGO_DB = 'yj_house_price'  # 选择的数据库
MONGO_COLLECTION = 'house_info'  # 选择表collection
# 创建一个MongoDB的连接对象
client = pymongo.MongoClient(MONGO_URL)
# 或者：pymongo.MongoClient(host='localhost', port=27017)
db = client[MONGO_DB]  # 选择数据库，或写成：client.yj_house_price
# 保存到MongoDB， param：result
def save_to_mongo(result):
    try:
        if db[MONGO_COLLECTION].insert_many(result):
            print('存储到MongoDB成功')
    except Exception:
        print('存储到MongoDb失败')


if __name__ == "__main__":
    houses_contents = []
    common_url = 'http://yangjiang.newhouse.fang.com/house/s/jiangchengqu/b9{}/?ctm=1.yangjiang.xf_search.page.{}'
    for i in range(1, 4):
        origin_url = common_url.format(i, i+1)  # 阳江江城区楼盘链接
        urls = get_houses_urls(origin_url)  # 获取上述链接对应的页面中所有楼盘的原页面链接
        for url in urls:
            houses_contents.append(get_house_info(url))  # 每个楼盘的信息
    save_to_mongo(houses_contents)  # 存储到MongoDB
