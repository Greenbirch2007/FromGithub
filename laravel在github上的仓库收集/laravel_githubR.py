#! -*- coding:utf-8 -*-
import datetime
import time

import pymysql
import requests
from lxml import etree
from selenium import webdriver

driver = webdriver.Chrome()
# 把find_elements 改为　find_element
def get_first_page():

    url = 'https://github.com/search?p=1&q=laravel&type=Repositories'
    driver.get(url)
    time.sleep(3)

    html = driver.page_source
    return html





# 把首页和翻页处理？

def next_page():
    for i in range(1,26):  # selenium 循环翻页成功！
        driver.find_element_by_xpath('//*[@id="js-pjax-container"]/div/div[3]/div/div[3]/div/a[last()]').click()
        time.sleep(1)
        html = driver.page_source
        return html

def rRound_block(item):
    f =" ".join(item.split())
    return f

def parse_html(html):  # 正则专门有反爬虫的布局设置，不适合爬取表格化数据！
    big_list = []
    selector = etree.HTML(html)
    name = selector.xpath('//*[@id="js-pjax-container"]/div/div[3]/div/ul/li/div[2]/div[1]/a/@href')
    link = selector.xpath('//*[@id="js-pjax-container"]/div/div[3]/div/ul/li/div[2]/div[1]/a/@href')

    descr = selector.xpath('//*[@id="js-pjax-container"]/div/div[3]/div/ul/li/div[2]/p/text()')
    star_n = selector.xpath('//*[@id="js-pjax-container"]/div/div[3]/div/ul/li/div[2]/div[2]/div[2]/div[1]/a/text()')

    for i1,i2,i3,i4 in zip(remove_block(name),link,remove_block(descr),remove_block(star_n)):
        big_list.append((i1,"https://github.com"+i2,rRound_block(i3),rRound_block(i4)))
    return big_list


        # 存储到MySQL中

def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456',
                                 db='github',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    try:
        cursor.executemany('insert into _laravel (name,link,descr,star_n) values (%s,%s,%s,%s)', content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except StopIteration:
        pass

def remove_douhao(num):
    num1 = "".join(num.split(","))
    f_num = str(num1)
    return f_num
def remove_block(items):
    new_items = []
    for it in items:
        f = "".join(it.split())
        new_items.append(f)
    return new_items



if __name__ == '__main__':
        html = get_first_page()
        content = parse_html(html)
        time.sleep(1)
        print(content)
        insertDB(content)
        while True:
            html = next_page()
            content = parse_html(html)
            insertDB(content)
            print(datetime.datetime.now())
            time.sleep(1)


# #name,link,descr,star_n
# create table _laravel(
# id int not null primary key auto_increment,
# name varchar(80),
# link varchar(88),
# descr text,
# star_n varchar(10)
# ) engine=InnoDB  charset=utf8;