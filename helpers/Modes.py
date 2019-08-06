#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:10521
# datetime:2019-08-03 3:05
# software: PyCharm
from peewee import *
from config import settings
import datetime

database = MySQLDatabase(
    database=settings.DATABASES['NAME'],
    user=settings.DATABASES['USER'],
    passwd=settings.DATABASES['PASSWORD'],
    host=settings.DATABASES['HOST'],
    port=settings.DATABASES['POST'],
    charset='utf8mb4'
)


class Model(Model):
    class Meta:
        database = database


class novels(Model):
    title = TextField()
    desc = TextField()
    author = TextField()
    novel_type_id = IntegerField()
    url = TextField()
    create_time = DateTimeField(default=datetime.datetime.now())
    update_time = DateTimeField(default=datetime.datetime.now())

    class Meta:
        db_table = 'books_novels'


class Assort(Model):
    title = TextField()
    create_time = DateTimeField(default=datetime.datetime.now())
    update_time = DateTimeField(default=datetime.datetime.now())

    class Meta:
        db_table = 'books_assort'
