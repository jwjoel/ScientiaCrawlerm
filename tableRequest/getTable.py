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

getTable = Blueprint('getTable',__name__)

@getTable.route('/getTable')
def _getTable():

        try:

                        time = request.args.get("time")
                        openid = request.args.get("openid")

                        db = pymysql.connect(
                        host="40.89.174.198",
                        port=3900,
                        user="jovel",
                        password='12321Wjwwjw',
                        database="jovel",
                        charset="utf8")
                        cursor = db.cursor()

                        cursor.execute("SELECT * FROM user WHERE wxUser = '"+openid+"'")
                        tempSql = cursor.fetchone()
                        username = tempSql[2]
                        password = tempSql[3]

        
                        data = {'__LASTFOCUS':'', 
                                '__VIEWSTATE':'/wEPDwUJLTczNTI4NDAyD2QWAgIED2QWAgIBD2QWDgIBDw8WAh4EVGV4dAUFTG9naW5kZAIDDw8WAh8ABSlQbGVhc2UgcHJvdmlkZSB5b3VyIHVzZXJuYW1lIGFuZCBwYXNzd29yZGRkAgUPDxYCHwAFCVVzZXIgTmFtZWRkAgkPDxYCHwAFCFBhc3N3b3JkZGQCDQ8PFgIfAGVkZAIPDw8WAh8ABQVMb2dpbmRkAhEPDxYCHgdWaXNpYmxlaGRkZBDCVKyf3AlB4U5faD0nkFSvTSj0', 
                                '__VIEWSTATEGENERATOR':'E17C8BF4', 
                                '__EVENTTARGET':'',
                                '__EVENTARGUMENT':'', 
                                '__EVENTVALIDATION':'/wEWBAKlxqv6DAKjq9T8DgLL9PDwDAKa/J78DjPkRpdQ5ncL0EHTxJDwo5F67wym', 
                                'tUserName':username,
                                'tPassword':password, 
                                'bLogin':'Login'
                                }
                        headers = {'User-agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Mobile Safari/537.36',
                                'Content-Type':'application/x-www-form-urlencoded',
                                'Host':'onlinetimetables.bham.ac.uk'}
                        login_url = 'https://onlinetimetables.bham.ac.uk/timetable/current_academic_year_2/login.aspx'
                        session = requests.Session()
                        resp = session.post(login_url, data,verify=False)

                        tree=etree.HTML(resp.content.decode('utf-8'))
                        div=tree.xpath('//*[@id="__VIEWSTATE"]/@value')[0]
                        VIEWSTATE = urllib.parse.quote(div,safe='')
                        VIEWSTATE = div
                        tree=etree.HTML(resp.content.decode('utf-8'))
                        div=tree.xpath('//*[@id="__VIEWSTATEGENERATOR"]/@value')[0]
                        VIEWSTATEGENERATOR = urllib.parse.quote(div,safe='')
                        VIEWSTATEGENERATOR = div
                        tree=etree.HTML(resp.content.decode('utf-8'))
                        div=tree.xpath('//*[@id="__EVENTVALIDATION"]/@value')[0]
                        EVENTVALIDATION = urllib.parse.quote(div,safe='')
                        EVENTVALIDATION = div

                        data= { '__EVENTTARGET':'LinkBtn_mystudentset',
                                '__EVENTARGUMENT':'',
                                '__VIEWSTATE':VIEWSTATE,
                                '__VIEWSTATEGENERATOR':VIEWSTATEGENERATOR,
                                '__EVENTVALIDATION':EVENTVALIDATION,
                                'tLinkType':'informationLanding'}
                        url='https://onlinetimetables.bham.ac.uk/Timetable/current_academic_year_2/default.aspx'
                        resp = session.post(url, data, verify=False)
                        #print(resp.content.decode('utf-8'))
                        tree=etree.HTML(resp.content.decode('utf-8'))
                        div=tree.xpath('//*[@id="__VIEWSTATE"]/@value')[0]
                        VIEWSTATE = urllib.parse.quote(div,safe='')
                        VIEWSTATE = div
                        tree=etree.HTML(resp.content.decode('utf-8'))
                        div=tree.xpath('//*[@id="__VIEWSTATEGENERATOR"]/@value')[0]
                        VIEWSTATEGENERATOR = urllib.parse.quote(div,safe='')
                        VIEWSTATEGENERATOR = div
                        tree=etree.HTML(resp.content.decode('utf-8'))
                        div=tree.xpath('//*[@id="__EVENTVALIDATION"]/@value')[0]
                        EVENTVALIDATION = urllib.parse.quote(div,safe='')
                        EVENTVALIDATION = div
                        div=tree.xpath('//*[@id="tUser"]/@value')[0]
                        tUser = div
                        tree=etree.HTML(resp.content.decode('utf-8'))
                        div=tree.xpath('//*[@id="lbWeeks"]/option[contains(text(),"Current")]/@value')[0]
                        
                        currentweek = int(div)
                        week = int(time) + int(div)
                        
                        url='https://onlinetimetables.bham.ac.uk/Timetable/current_academic_year_2/default.aspx'
                        data={'__EVENTTARGET':'','__EVENTARGUMENT':'',
                                '__LASTFOCUS':'','__VIEWSTATE':VIEWSTATE,
                                '__VIEWSTATEGENERATOR':VIEWSTATEGENERATOR,'__EVENTVALIDATION':EVENTVALIDATION,
                                'tLinkType':'mystudentset','tUser':tUser,'lbWeeks':' '+str(week),'lbDays':'1-5',
                                'dlPeriod':'3-22','dlType':'TextSpreadsheet;swsurl;SWSCUST Object TextSpreadsheet',
                                'bGetTimetable':'View Timetable'}
                        resp = session.post(url,data, verify=False)
                        #print(resp.content.decode('utf-8'))
                        outJson = ''
                        idNum = 0
                        
                        tree=etree.HTML(resp.content.decode('utf-8'))

                        ifExist = tree.xpath('//table[2]/tr[1]/td[2]')
                        
                        try:
                                test = ifExist[0].text
                                extMonday = 3
                                existMon = True
                        except:
                                existMon = False
                                extMonday = 2

                        ifExist = tree.xpath('//table[3]/tr[1]/td[2]')
                        try:    
                                test = ifExist[0].text
                                extTuesday = extMonday + 1
                                existTue = True
                        except:
                                existTue = False
                                extTuesday = extMonday

                        ifExist = tree.xpath('//table[4]/tr[1]/td[2]')
                        try:    
                                test = ifExist[0].text
                                extWednesday = extTuesday + 1
                                existWed = True
                        except:
                                existWed = False
                                extWednesday = extTuesday

                        ifExist = tree.xpath('//table[5]/tr[1]/td[2]')
                        try:    
                                test = ifExist[0].text
                                extThuesday = extWednesday + 1
                                existThu = True
                        except:
                                existThu = False
                                extThuesday = extWednesday
                        ifExist = tree.xpath('//table[6]/tr[1]/td[2]')
                        try:    
                                test = ifExist[0].text
                                extFriday = extThuesday + 1
                                existFri = True
                        except:
                                existFri = False
                                extFriday = extThuesday

                        def selectcolor(oldcolor,name):
                                color = ''
                                seminar = "Seminar"
                                lecture = "Lecture"
                                tutorial = "Tutorial"
                                workshop = "Workshop"
                                exam = "Exam"
                                test = "Test"
                                if(test in name):
                                        color = "#dc3032"
                                elif(lecture in oldcolor):
                                        color = "#21a675"
                                elif(tutorial in oldcolor):
                                        color = "#8d4bbb"
                                elif(workshop in oldcolor):
                                        color = "#50616d"
                                elif(exam in oldcolor):
                                        color = "#dc3032"
                                elif(seminar in oldcolor):
                                        color = "#4b5cc4"
                                else:
                                        color = "#21a675"
                                return(color)

                        def shortname(starttime,endtime,fullname):
                                
                                timegap = 0
                                acceptlength = 0
                                temp=[]
                                temp = endtime.split(":", 1)
                                endtime = int(temp[0])
                                temp = starttime.split(":", 1)
                                starttime = int(temp[0])
                                timegap = int(endtime) - int(starttime)
                                acceptlength = int(timegap*11)
                                stname = ''

                                if(len(fullname) > acceptlength):
                                        stname = fullname[0:acceptlength] + '...'
                                else:
                                        stname = fullname
                                return(stname)


                        if existMon != False:   
                                
                                Monday = pd.read_html(resp.content.decode('utf-8'))[extMonday]
                                Line = Monday.shape[0] - 1
                                for i in range(1, Line + 1):
                                        Arry = Monday.loc[[i]]
                                        temp = Arry.values
                                        tempFir=temp.tolist()
                                        tempSec=tempFir[0]
                                        idNum = idNum + 1
                                        tempStart = tempSec[2].split(":", 1)
                                        Start = int(tempStart[0])
                                        tempEnd = tempSec[3].split(":", 2)
                                        if(tempEnd[1] != ''):
                                        	minNum = int(tempEnd[0]) + (int(tempEnd[1]) / 60)
                                        else:
                                        	minNum = int(tempEnd[0])
                                        End = minNum
                                       
                                        top = 45 + 120 * ( Start - 9 )
                                        height = ((End - Start) * 110) + ((End - Start - 1) * 10)
                                     
                                        data = {
                                                "Status":"Pass",
                                                "id":idNum,
                                                "date":"Null",
                                                "Activity":tempSec[0],
                                                "Type":tempSec[1],
                                                "Start":tempSec[2],
                                                "End":tempSec[3],
                                                "left":"6",
                                                "top":str(top),
                                                "height":str(height),
                                                "Room":tempSec[5],
                                                "Staff":str(tempSec[6]),
                                                "color":selectcolor(tempSec[1],tempSec[0]),
                                                "currentweek":str(currentweek),
                                                "shortname":shortname(tempSec[2],tempSec[3],tempSec[0])
                                        }
                                        if( idNum == 1 ):
                                                outJson = json.dumps(data)
                                        else:
                                                outJson = outJson + "," + json.dumps(data)

                        if existTue != False:   
                                Tuesday = pd.read_html(resp.content.decode('utf-8'))[extTuesday]
                                Line = Tuesday.shape[0] - 1

                                for i in range(1, Line + 1):
                                        Arry = Tuesday.loc[[i]]
                                        temp = Arry.values
                                        tempFir=temp.tolist()
                                        tempSec=tempFir[0]
                                        idNum = idNum + 1
                                        tempStart = tempSec[2].split(":", 1)
                                        Start = int(tempStart[0])
                                        tempEnd = tempSec[3].split(":", 1)
                                        tempEnd = tempSec[3].split(":", 2)
                                        if(tempEnd[1] != ''):
                                        	minNum = int(tempEnd[0]) + (int(tempEnd[1]) / 60)
                                        else:
                                        	minNum = int(tempEnd[0])
                                        End = minNum
                                        top = 45 + 120 * ( Start - 9 )
                                        height = ((End - Start) * 110) + ((End - Start - 1) * 10)
                                        data = {
                                                "Status":"Pass",
                                                "id":idNum,
                                                "date":"Null",
                                                "Activity":tempSec[0],
                                                "Type":tempSec[1],
                                                "Start":tempSec[2],
                                                "End":tempSec[3],
                                                "left":"135",
                                                "top":top,
                                                "height":str(height),
                                                "Room":tempSec[5],
                                                "Staff":str(tempSec[6]),
                                                "color":selectcolor(tempSec[1],tempSec[0]),
                                                "currentweek":str(currentweek),
                                                "shortname":shortname(tempSec[2],tempSec[3],tempSec[0])
                                        }
                                        if( idNum == 1 ):
                                                outJson = json.dumps(data)
                                        else:
                                                outJson = outJson + "," + json.dumps(data)

                        if existWed != False:  
                                Wednesday = pd.read_html(resp.content.decode('utf-8'))[extWednesday]
                                Line = Wednesday.shape[0] - 1

                                for i in range(1, Line + 1):
                                        Arry = Wednesday.loc[[i]]
                                        temp = Arry.values
                                        tempFir=temp.tolist()
                                        tempSec=tempFir[0]
                                        idNum = idNum + 1
                                        tempStart = tempSec[2].split(":", 1)
                                        Start = int(tempStart[0])
                                        tempEnd = tempSec[3].split(":", 1)
                                        tempEnd = tempSec[3].split(":", 2)
                                        if(tempEnd[1] != ''):
                                        	minNum = int(tempEnd[0]) + (int(tempEnd[1]) / 60)
                                        else:
                                        	minNum = int(tempEnd[0])
                                        End = minNum
                                        top = 45 + 120 * ( Start - 9 )
                                        height = ((End - Start) * 110) + ((End - Start - 1) * 10)
                                        data = {
                                                "Status":"Pass",
                                                "id":idNum,
                                                "date":"Null",
                                                "Activity":tempSec[0],
                                                "Type":tempSec[1],
                                                "Start":tempSec[2],
                                                "End":tempSec[3],
                                                "left":"263",
                                                "top":top,
                                                "height":str(height),
                                                "Room":tempSec[5],
                                                "Staff":str(tempSec[6]),
                                                "color":selectcolor(tempSec[1],tempSec[0]),
                                                "currentweek":str(currentweek),
                                                "shortname":shortname(tempSec[2],tempSec[3],tempSec[0])
                                        }
                                        if( idNum == 1 ):
                                                outJson = json.dumps(data)
                                        else:
                                                outJson = outJson + "," + json.dumps(data)

                        if existThu != False:
                                Thuesday = pd.read_html(resp.content.decode('utf-8'))[extThuesday]
                                Line = Thuesday.shape[0] - 1

                                for i in range(1, Line + 1):
                                        Arry = Thuesday.loc[[i]]
                                        temp = Arry.values
                                        tempFir=temp.tolist()
                                        tempSec=tempFir[0]
                                        idNum = idNum + 1
                                        tempStart = tempSec[2].split(":", 1)
                                        Start = int(tempStart[0])
                                        tempEnd = tempSec[3].split(":", 1)
                                        tempEnd = tempSec[3].split(":", 2)
                                        if(tempEnd[1] != ''):
                                        	minNum = int(tempEnd[0]) + (int(tempEnd[1]) / 60)
                                        else:
                                        	minNum = int(tempEnd[0])
                                        End = minNum
                                        top = 45 + 120 * ( Start - 9 )
                                        height = ((End - Start) * 110) + ((End - Start - 1) * 10)
                                        data = {
                                                "Status":"Pass",
                                                "id":idNum,
                                                "date":"Null",
                                                "Activity":tempSec[0],
                                                "Type":tempSec[1],
                                                "Start":tempSec[2],
                                                "End":tempSec[3],
                                                "left":"392",
                                                "top":top,
                                                "height":str(height),
                                                "Room":tempSec[5],
                                                "Staff":str(tempSec[6]),
                                                "color":selectcolor(tempSec[1],tempSec[0]),
                                                "currentweek":str(currentweek),
                                                "shortname":shortname(tempSec[2],tempSec[3],tempSec[0])
                                        }
                                        if( idNum == 1 ):
                                                outJson = json.dumps(data)
                                        else:
                                                outJson = outJson + "," + json.dumps(data)

                        if existFri != False:
                                Friday = pd.read_html(resp.content.decode('utf-8'))[extFriday]
                                Line = Friday.shape[0] - 1

                                for i in range(1, Line + 1):
                                        Arry = Friday.loc[[i]]
                                        temp = Arry.values
                                        tempFir=temp.tolist()
                                        tempSec=tempFir[0]
                                        idNum = idNum + 1
                                        tempStart = tempSec[2].split(":", 1)
                                        Start = int(tempStart[0])
                                        tempEnd = tempSec[3].split(":", 1)
                                        tempEnd = tempSec[3].split(":", 2)
                                        if(tempEnd[1] != ''):
                                        	minNum = int(tempEnd[0]) + (int(tempEnd[1]) / 60)
                                        else:
                                        	minNum = int(tempEnd[0])
                                        End = minNum
                                        top = 45 + 120 * ( Start - 9 )
                                        height = ((End - Start) * 110) + ((End - Start - 1) * 10)
                                        data = {
                                                "Status":"Pass",
                                                "id":idNum,
                                                "date":"Null",
                                                "Activity":tempSec[0],
                                                "Type":tempSec[1],
                                                "Start":tempSec[2],
                                                "End":tempSec[3],
                                                "left":"520",
                                                "top":top,
                                                "height":str(height),
                                                "Room":tempSec[5],
                                                "Staff":str(tempSec[6]),
                                                "color":selectcolor(tempSec[1],tempSec[0]),
                                                "currentweek":str(currentweek),
                                                "shortname":shortname(tempSec[2],tempSec[3],tempSec[0])
                                        }
                                        if( idNum == 1 ):
                                                outJson = json.dumps(data)
                                        else:
                                                outJson = outJson + "," + json.dumps(data)
                                outJson = "[ " + outJson + " ]"

                        return(outJson)
        except:
                        data = {
                                "Status":"Fail",
                        }
                        return(json.dumps(data))
                        

        return(outJson)
