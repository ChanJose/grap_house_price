# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

url = 'https://yjgjjrzx0662.fang.com/'
headers = {
    'User-Agent': 'Mozilla/5.0(Macintosh;Intel Mac OS X 10_12_6) AppleWebKit/537.36(KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
}
response = requests.get(url, headers=headers)
houses_content = {}  # 存储房子信息
if response.status_code == 200:
    html = response.text.encode("latin1").decode("gbk")
    soup = BeautifulSoup(html, "html.parser")  # 解析
    information = soup.select(".information")[0]
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
    houses_content['开盘时间'] = information.select(".information_li .kaipan")[0].text  # 开盘时间
print(houses_content)