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

from flask import Blueprint

bind = Blueprint('bind',__name__)

@bind.route('/bind')
def _bind():
    #This part is use for storage userdata to database, If you don't need it, just ignore.
    try:
        db = pymysql.connect(
        host="",
        port=3306,
        user="",
        password='',
        database="",
        charset="utf8")
        cursor = db.cursor()

        bindUser = request.args.get("user")
        bindPass = request.args.get("pass")
        openId = request.args.get("openid")
        cursor.execute('UPDATE user SET uniUser="' + bindUser + '" ,uniPass="' + bindPass + '" WHERE wxUser = "'+openId+'";')
        db.commit()
        #return('UPDATE user SET uniUser="' + bindUser + '" ,uniPass="' + bindPass + '" WHERE wxUser = "'+openId+'";')
        data={"Status":"Successful"}
        return(json.dumps(data))
        db.close()
    except:
        data={"Status":"Fail"}
        return(json.dumps(data))
