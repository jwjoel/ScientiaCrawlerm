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

wxLogin = Blueprint('wxLogin',__name__)

@wxLogin.route('/wxLogin')
def _wxLogin():
        #nickName = request.args.get("nickName")
        openid = request.args.get("openid")
        loginFail = False

        if(loginFail == False):
                try:
                        db = pymysql.connect(
                        host="127.0.0.1",
                        port=3900,
                        user="jovel",
                        password='12321Wjwwjw',
                        database="jovel",
                        charset="utf8")
                        cursor = db.cursor()
                        if (str(cursor.execute("SELECT * FROM user WHERE wxUser = '"+openid+"'")) == "0"):
                                cursor.execute('INSERT INTO user VALUES (0, "'+openid+'", "Empty", "Empty", "Empty", "Empty", "[]")')
                                db.commit()
                                data = {"Status":"uniRequired", "openid":openid}
                                return(json.dumps(data))
                        else:
                                cursor.execute("SELECT * FROM user WHERE wxUser = '"+openid+"'")
                                tempSql = cursor.fetchone()
                                uniUser = tempSql[2]
                                uniPass = tempSql[3]
                                if(uniUser == "Empty" or uniPass == "Empty"):
                                        data = {"Status":"uniRequired", "openid":openid}
                                        return(json.dumps(data))
                                else:
                                        data = {"Status":"Pass", "uniUser":uniUser, "uniPass":uniPass, "openid":openid}
                                        return(json.dumps(data))

                                
                        db.close()
                except:
                        data={"Status":"SqlError"}
                        return(json.dumps(data))
        else:
                data={"Status":"LoginError"}
                return(json.dumps(data))
