#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:10521
# datetime:2019-08-02 23:46
# software: PyCharm
from requests_html import HTMLSession
from bs4 import BeautifulSoup

import re


class qiShuWang(object):

    def __init__(self):
        self._url = 'https://wap.qisuu.la'
        self._http = HTMLSession()
        self._headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'User-Agent:': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
        }
        self._sort = []

    def get_classification(self):
        """
        获取分类
        :return:
        """
        res = self._http.get(self._url + '/sort.html', timeout=10)

        if res.status_code != 200:
            return f'请求code码错误{res.status_code}'
        res.encoding = 'uft-8'
        bs4 = BeautifulSoup(res.text, 'lxml')

        menu_nav = bs4.find('div', attrs={'class': 'menu_nav'})
        if menu_nav in [None]:
            return f'获取分类失败'
        li = menu_nav.find_all('li')
        data = []
        for i, value in enumerate(li):
            # 获取总页数
            res = self._http.get(f'{self._url}{value.a["href"]}')
            if res.status_code != 200:
                page = '获取失败'
            else:
                page = re.findall(r'(第(\d.*?)/(\d.*?)页)', res.text)
                if len(page) == 1 and len(page[0]) == 3:
                    page = int(page[0][2])
                else:
                    page = '获取失败'
            data.append({'name': value.text, 'href': value.a['href'], 'page': page})
        self._sort = data
        return self._sort

    def get_books(self, url):
        """
        :param url:
        :return:
        """
        _books = []
        res = self._http.get(f'{self._url}{url}', timeout=10)
        if res.status_code != 200:
            return f'响应码错误{res.status_code}'
        bs4 = BeautifulSoup(res.text, 'lxml')
        article = bs4.find_all('div', attrs={'class': 'article'})
        # 获取页数
        page = bs4.find('div', attrs={'class': 'page'}).find_all('a')
        if len(page) in [[]]:
            return '采集获取页数失败'
        # 获取书籍详情页面
        for _value in article:
            details = {}
            pic = _value.find('div', attrs={'class': 'pic'})
            title = _value.find('h6').text
            author = _value.find('p', attrs={'class': 'author'}).a.text
            simple = _value.find('p', attrs={'class': 'simple'}).text
            details.update({'href': pic.a['href']})
            details.update({'scr': pic.img['src']})
            details.update({'title': title})
            details.update({'author': author})
            details.update({'simple': simple})
            _books.append(details)
        return _books


qiShuWang = qiShuWang()
