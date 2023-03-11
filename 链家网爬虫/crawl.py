from xpinyin import Pinyin
import requests
import time
import random
from lxml import etree
import pandas as pd


# import logging
# from log import record

def crawl_city(city):
    pin = Pinyin()
    url_head = r'https://' + ''.join([x[0] for x in pin.get_pinyin(city).split('-')]) + r'.lianjia.com/ershoufang/pg'
    links = []
    for i in range(1, 101):  # range(1,101) cost too long time
        url = url_head + str(i)
        print(url)
        response = requests.get(url)
        time.sleep(random.random())
        time.sleep(random.randint(5, 8))  # sleep more time
        # print(response.text)
        data = etree.HTML(response.text)
        for j in range(1, 31):
            link = data.xpath(r'/html/body/div[4]/div[1]/ul/li[' + str(j) + r']/div[1]/div[1]/a/@href')
            links.append(link[0])

    houses = []
    print("num of links :", len(links))
    for link in links:
        print(link)
        response = requests.get(link)
        time.sleep(random.random())
        time.sleep(random.randint(5, 8))  # sleep more time
        data = etree.HTML(response.text)
        house = {"城市": city, "链接": link}
        for i in range(1, 13):
            key = data.xpath(r'/ html / body / div[7] / div[1] / div[1] / div / div / div[1] / div[2] / ul / li['
                             + str(i) + r'] / span / text()')
            value = data.xpath(r'/ html / body / div[7] / div[1] / div[1] / div / div / div[1] / div[2] / ul / li['
                               + str(i) + r'] / text()')

            if len(key) < 1:
                key = data.xpath(r'/ html / body / div[7] / div[2] / div[1] / div / div / div[1] / div[2] / ul / li['
                                 + str(i) + r'] / span / text()')
                value = data.xpath(r'/ html / body / div[7] / div[2] / div[1] / div / div / div[1] / div[2] / ul / li['
                                   + str(i) + r'] / text()')

            if len(key) < 1:
                continue
            # print(key, value)
            house[key[0]] = value[0]

        for i in range(1, 9):
            key = data.xpath(r'/ html / body / div[7] / div[1] / div[1] / div / div / div[2] / div[2] / ul / li['
                             + str(i) + r'] / span[1] / text()')
            value = data.xpath(r'/ html / body / div[7] / div[1] / div[1] / div / div / div[2] / div[2] / ul / li['
                               + str(i) + r'] / span[2] / text()')
            if len(key) < 1:
                key = data.xpath(r'/ html / body / div[7] / div[2] / div[1] / div / div / div[2] / div[2] / ul / li['
                                 + str(i) + r'] / span[1] / text()')
                value = data.xpath(r'/ html / body / div[7] / div[2] / div[1] / div / div / div[2] / div[2] / ul / li['
                                   + str(i) + r'] / span[2] / text()')
            if len(key) < 1:
                continue
            house[key[0]] = value[0]

        if len(house) < 2:
            continue

        value = data.xpath(r'/html/body/div[5]/div[2]/div[3]/div/span[1]/text()')

        # print(type(value), value)
        # print(type(value[0]), value[0])
        value = float(value[0])*1e4
        # print(type(value), value)

        house["价格（单位：人民币）"] = value

        houses.append(house)

        tmp_df = pd.DataFrame(houses)
        tmp_df.to_csv('tmp.csv')
        # print(len(house))
        # print(house)
    df = pd.DataFrame(houses)
    return df


def crawl():
    capitals = {'湖南': '长沙', '湖北': '武汉', '广东': '广州', '广西': '南宁', '河北': '石家庄', '河南': '郑州', '山东': '济南',
                '山西': '太原', '江苏': '南京', '浙江': '杭州', '江西': '南昌', '黑龙江': '哈尔滨', '新疆': '乌鲁木齐', '云南': '昆明',
                '贵州': '贵阳', '福建': '福州', '吉林': '长春', '安徽': '合肥', '四川': '成都', '西藏': '拉萨', '宁夏': '银川',
                '辽宁': '沈阳', '青海': '西宁', '甘肃': '兰州', '陕西': '太原', '内蒙古': '呼和浩特', '台湾': '台北', '北京': '北京',
                '上海': '上海', '天津': '天津', '重庆': '重庆', '香港': '香港', '澳门': '澳门'}

    for province, capital in capitals.items():
        if not os.path.exists(r'./database'):
            os.mkdir(r'./database')
        df = crawl_city(capital)
        df.to_csv(r'./database/' + capital + ".csv", index=False)
        # logger_info = record(filename='./log.txt', level=logging.INFO)
        # logger_info.info("爬取信息已保存至" + r'./database/' + capital+".csv")


if __name__ == "__main__":
    crawl_city("沈阳").to_csv('沈阳.csv')
