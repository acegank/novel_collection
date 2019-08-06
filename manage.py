#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:10521
# datetime:2019-08-03 2:39
# software: PyCharm
from public.qishuwang import qiShuWang
import time
import threading
import queue
from config import settings
from multiprocessing.pool import ThreadPool
from helpers.Modes import novels, Assort

THREAD_LIMIT = settings.THREADS_COUNT  # 设置线程数
Queue = queue.Queue()
lock = threading.Lock()  # 设置一个线程锁
pool = ThreadPool(THREAD_LIMIT)


def run():
    try:

        for i, value in enumerate(qiShuWang.get_classification()):
            # qiShuWang.get_books(value['name'], value['href'])
            print("小说类型：", value['name'], f'共有页数:{value["page"]}')

            # 设置加入队列
            for ii in range(1, value['page'] + 1):
                Queue.put(f"{value['href']}index_{ii}.html")

            threads = [pool.apply_async(directory_storage, (Queue.get(), value['name']))
                       for _ in range(Queue.qsize())]

            for thread in threads:
                thread.wait()  # 等待线程函数执行完毕
            pool.close()  # 关闭线程池
            pool.join()
        # for queues in range(1, queue.qsize + 1)

    except Exception as _error:
        print('Exception', _error)


def directory_storage(urls, name):
    """
    :param urls: 采集url
    :param name: 分类
    :return:
    """
    res = qiShuWang.get_books(urls)
    print(res)
    time.sleep(1)


# novel_type = ''
#             # 寻找对绑定的一级分类ID
#             for __value in _assort_data.keys():
#                 if __name == __value:
#                     novel_type = _assort_data[__value]
#                     break
#
#             for __value in _books:
#                 # 判断是否已经入库
#                 chapter = novels.select('*').where(novels.title == __value['title'])
#
#                 if chapter.count() <= 0:
#                     data = [
#                         {
#                             'title': __value['title'],
#                             'desc': __value['simple'],
#                             'author': __value['author'],
#                             'novel_type_id': novel_type,
#                             'url': __value['scr']
#                         }
#                     ]
#                     model = novels.insert_many(data).execute()
#                     print(f"{__value['title']}---{model}")
#                 else:
#                     print(f"{__value['title']}---小说已经入库")
#
#             _books = []
#             if maximum != 'all' and int(maximum) == _i:
#                 break

if __name__ == '__main__':
    print(Assort.select("*"))
    # run()
