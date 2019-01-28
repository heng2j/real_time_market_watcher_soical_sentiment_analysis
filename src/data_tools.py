#!/usr/bin/env python3
# consumer_news.py
# ---------------
# Author: Zhongheng Li
# Start Date: 01-03-19
# Last Modified Date: 01-23-19


"""
This code save real time news data to AWS DynamoDB in every 15 mins

"""

# System modules
import configparser
import os
from os.path import dirname as up
import sys

# 3rd party modules
from sqlalchemy import create_engine


projectPath = os.getcwd()
DB_configs_ini_file_path = projectPath + "/src/DB/db_configs.ini"

print("DB_configs_ini_file_path: ", DB_configs_ini_file_path)


def getSQL_DB_Engine( filePath=None):
    """

    :param filePath: DB configs ini file path
    :return: SQLalchemy database engine
    """

    config = configparser.ConfigParser()
    config.read(DB_configs_ini_file_path)

    DB_TYPE = config['DB_Configs']['DB_TYPE']
    DB_DRIVER = config['DB_Configs']['DB_DRIVER']
    DB_USER = config['DB_Configs']['DB_USER']
    DB_PASS = config['DB_Configs']['DB_PASS']
    DB_HOST = config['DB_Configs']['DB_HOST']
    DB_PORT = config['DB_Configs']['DB_PORT']
    DB_NAME = config['DB_Configs']['DB_NAME']
    SQLALCHEMY_DATABASE_URI = '%s+%s://%s:%s@%s:%s/%s' % (DB_TYPE, DB_DRIVER, DB_USER,
                                                          DB_PASS, DB_HOST, DB_PORT, DB_NAME)
    engine = create_engine(
        SQLALCHEMY_DATABASE_URI, echo=False)

    return engine
