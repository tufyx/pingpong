'''
Created on 25 Aug 2014

@author: tufyx
'''

CSRF_ENABLED = False
SECRET_KEY = 'thequickbrownfoxjumpsoverthelazydog'

#CONFIG MYSQL
MYSQL_HOST = 'dev.tufyx.com'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'Test1234'

import os
basedir = os.path.abspath(os.path.dirname(__file__))
APP_ROOT = os.path.dirname(__file__)

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://'+MYSQL_USER+':'+MYSQL_PASSWORD + '@' + MYSQL_HOST + '/pingpong'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')