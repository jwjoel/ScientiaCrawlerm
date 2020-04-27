from flask import Flask
from flask import request
import requests
import sys
import io
from lxml import etree
import urllib.parse
import pandas as pd
import json
import pymysql
from tableRequest.getTable import getTable
from basicAccount.bindUni import bind
from basicAccount.wxLogin import wxLogin

app = Flask(__name__)

@app.route('/')
def index():
    return 'TimeScope | Ver 1.5'

app.register_blueprint(getTable)
app.register_blueprint(bind)
app.register_blueprint(wxLogin)


if __name__ == '__main__':

    app.run('0.0.0.0', port=443, ssl_context=('wechat.pem', 'wechat.key'))