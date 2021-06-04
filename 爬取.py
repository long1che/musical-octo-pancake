#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/5 16:08
# @Author : loong
# @File : 爬取.py
# @Software: PyCharm

# -*- coding:utf-8 -*-
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib import parse
import time
import pymysql


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
# browser = webdriver.Chrome(chrome_options=chrome_options)
browser = webdriver.Chrome(executable_path='./chromedriver.exe',chrome_options=chrome_options)
wait = WebDriverWait(browser, 10)


def get_url(n, word, pinpai):
    print('正在爬取第' + str(n) + '页')
    # 确定搜索商品的内容
    keyword = {'keyword': word}
    # 页面n与参数page的关系
    page = '&page=%s' % (2 * n - 1)
    pinpai = '&ev=exbrand_%s' % (pinpai)
    url = 'https://search.jd.com/Search?'+parse.urlencode(keyword) + pinpai + '&enc=utf-8' + page
    print(url)
    return url


def parse_page(url, pinpai):
    print('爬取信息并保存中...')
    browser.get(url)
    # 把滑轮慢慢下拉至底部，触发ajax
    for y in range(100):
        js = 'window.scrollBy(0,100)'
        browser.execute_script(js)
        time.sleep(0.1)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#J_goodsList .gl-item')))
    html = browser.page_source
    soup = BeautifulSoup(html, 'lxml')
    # 找到所有商品标签
    goods = soup.find_all('li', class_="gl-item")
    # 遍历每个商品，得到每个商品的信息
    for good in goods:
        num = good['data-sku']
        tag = good.find('div', class_="p-price").strong.em.string
        money = good.find('div', class_="p-price").strong.i.string
        # 就是京东有些商品竟然没有店铺名，导检索store时找不到对应的节点导致报错
        store = good.find('div', class_="p-shop").span
        commit = good.find('div', class_="p-commit").strong.a.string
        name = good.find('div', class_="p-name p-name-type-2").a.em
        image = good.find('div', class_="p-img").a.img.get('src')
        detail_addr = good.find('div', class_="p-img").find('a')['href']

        if store is not None:
            new_store = store.a.string
        else:
            new_store = '没有找到店铺 - -！'
        new_name = ''
        for item in name.strings:
            new_name = new_name + item
        product = (num, pinpai, new_name, money, new_store, commit, image, detail_addr)
        save_to_mysql(product)
        print(product)


def save_to_mysql(result):
    # db = pymysql.connect("localhost", "root", "", "jd")
    db=pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='jd', charset='utf8')
    cursor = db.cursor()  # 使用cursor()方法获取操作游标
    sql = "INSERT INTO jdsj(info_num,info_brand,info_name,info_money,info_store,info_commit,info_image,info_detail) \
            VALUES ('%s','%s', '%s','%s', '%s','%s', '%s', '%s')" % \
          (result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7])
    try:
        cursor.execute(sql)  # 执行sql语句
        db.commit()  # 提交到数据库执行
        print('保存成功！')
    except:
        db.rollback()  # 发生错误时回滚
        print('保存失败！')
    db.close()  # 关闭数据库连接


def main():
    try:
        word = input('请输出你想要爬取的商品：')
        pinpai = input('请输出你想要爬取的品牌：')
        pages = int(input('请输入你想要抓取的页数(范围是1-100):'))

        # 京东最大页面数为100
        if 1 <= pages <= 100:
            page = pages + 1
            for n in range(1, page):
                url = get_url(n, word, pinpai)
                parse_page(url, pinpai)
            print('爬取完毕！')
            browser.close()
        else:
            print('请重新输入！')
            main()
    except Exception as error:
        print('出现异常！', error)
        return None


if __name__ == '__main__':
    main()
