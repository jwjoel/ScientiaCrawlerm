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
import datetime;
import random;

createGroup = Blueprint('createGroup',__name__)

@createGroup.route('/createGroup')
def _createGroup():

    def random()
        nowTime=datetime.datetime.now().strftime("%S%H%M")
        randomNum=random.randint(0,100)
        if randomNum<=10:
            randomNum=str(0)+str(randomNum)
        uniqueNum=str(nowTime)+str(randomNum)
        return(uniqueNum)

    name = request.args.get("name")
    avatar = request.args.get("avatar")
    info = request.args.get("info")
    owner = request.args.get("openid")
    permission = request.args.get("permission")
    createTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    groupid = random()
    userlist = []
    db = pymysql.connect(
    host="127.0.0.1",
    port=3306,
    user="TimeScope",
    password='12321Wjwwjw',
    database="TimeScope",
    charset="utf8")
    cursor = db.cursor()
    
    cursor.execute('INSERT INTO group VALUES (0, "'+name+'", "'+groupid+'", "'+avatar+'", "'+info+'", "'+owner+'", "' + userlist.append(owner) + '", "'+createTime+'", "'+permission+'")')
    db.commit()
    userlist = cursor.execute("SELECT groupID FROM user WHERE wxUser = '"+owner+"'")
    userlist.append(groupid)
    cursor.execute('UPDATE user SET groupID="' + userlist + '" WHERE wxUser = "'+owner+'"')
    db.commit()
    data={"Status":"Successful"}
    return(json.dumps(data))
    db.close()

@listGroup.route('/listGroup')
def _listGroup():

    user = request.args.get("openid")

    db = pymysql.connect(
    host="40.89.174.198",
    port=3900,
    user="jovel",
    password='12321Wjwwjw',
    database="jovel",
    charset="utf8")
    cursor = db.cursor()
    grouplist = cursor.execute("SELECT groupID FROM user WHERE wxUser = '"+user+"'")
    for i in len(grouplist):
        groupid = grouplist[i]
        groupinfo = cursor.execute("SELECT * FROM group WHERE groupID = '"+groupid+"'")

    data={"Name":groupinfo[1],
          "groupId":"Successful",
          "avatar":"Successful",
          "basicinfo":"Successful",
          "owner":"Successful",
          "users":"Successful",
          "permission":"Successful",
        }
    return(json.dumps(data))
    db.close()

@joinGroup.route('/joinGroup')
def _joinGroup():

    cursor = db.cursor()
    groupid = request.args.get("groupid")
    user = request.args.get("openid")

    db = pymysql.connect(
    host="40.89.174.198",
    port=3900,
    user="jovel",
    password='12321Wjwwjw',
    database="jovel",
    charset="utf8")

    userlist = cursor.execute("SELECT Users FROM group WHERE groupId = '"+groupid+"'")
    if user in userlist:
        data={"Status":"Exist"}
        return(json.dumps(data))
    else:
        userlist.append(user)
        cursor.execute('UPDATE group SET user="' + userlist + '" WHERE groupId = "'+groupid+'"')
        db.commit()
        userlist = cursor.execute("SELECT groupID FROM user WHERE wxUser = '"+user+"'")
        userlist.append(groupid)
        cursor.execute('UPDATE user SET groupID="' + userlist + '" WHERE wxUser = "'+user+'"')
        db.commit()
        data={"Status":"Successful"}
        return(json.dumps(data))
        db.close()

@exitGroup.route('/exitGroup')
def _exitGroup():

    cursor = db.cursor()
    groupid = request.args.get("groupid")
    user = request.args.get("openid")

    db = pymysql.connect(
    host="40.89.174.198",
    port=3900,
    user="jovel",
    password='12321Wjwwjw',
    database="jovel",
    charset="utf8")

    userlist = cursor.execute("SELECT Users FROM group WHERE groupId = '"+groupid+"'")
    if user in userlist:
        userlist.remove(user)
        cursor.execute('UPDATE group SET user="' + userlist + '" WHERE groupId = "'+groupid+'"')
        db.commit()
        userlist = cursor.execute("SELECT groupID FROM user WHERE wxUser = '"+user+"'")
        userlist.remove(groupid)
        cursor.execute('UPDATE user SET groupID="' + userlist + '" WHERE wxUser = "'+user+'"')
        db.commit()
        data={"Status":"Successful"}
        return(json.dumps(data))
        db.close()
    else:
        data={"Status":"notExist"}
        return(json.dumps(data))

