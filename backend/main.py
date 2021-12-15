#!/usr/bin/env python
# encoding: utf-8
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2,jinja2,os
import urllib
import json
import random
import logging
import re
import datetime
import time
import array
import csv
from google.appengine.ext import ndb
from google.appengine.api import images
from google.appengine.api import urlfetch
from google.appengine.api import mail
import gspread
import requests
from requests_toolbelt.adapters import appengine
from oauth2client.service_account import ServiceAccountCredentials

import sendgrid
from sendgrid.helpers import mail

appengine.monkeypatch()

JINJA_ENVIRONMENT = jinja2.Environment(
loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
extensions=['jinja2.ext.autoescape'],
autoescape=True)

GAME_LINK = "https://campaign.nextdigital.com.hk/roadshow-game/index.html"
TOTALGIFT = 3
COUNTER_NAME = "CURRENT"

@ndb.transactional(xg=True)
def addCounterAndSave(currentIndex,**kwds):
    # entity = User.query().fetch()
    # print entity
    try:
        Counter(id="CURRENT",COUNTER_NAME='CURRENT',INDEX=currentIndex).put()
        Winner(**kwds).put()
        #Location(key_name=poption,NAME=poption,SLOT=total_slot,SELECTED=total_selected+1).put()
        return "SUCCESS"
    except :
        return "FAIL"

@ndb.transactional
def getCurrentCount():
    entity = Counter.get_by_id('CURRENT')
    if entity == None :
        Counter(COUNTER_NAME='CURRENT', INDEX=0, id='CURRENT').put()
        return 0
    else:
        return entity.INDEX + 1

def checkEmailDuplication(email):
    duplicate_count = User.query(User.EMAIL == email).fetch()
    if len(duplicate_count) > 0 :
        return "true"

def checkPhoneDuplication(phone):
    duplicate_count = User.query(User.PHONE == phone).fetch()
    if len(duplicate_count) > 0 :
        return "true"

def checkSlot(target):
    return User.all().filter("OPTION = ",target).count()

def stillHaveGift():
    havegift = Gift.all().filter("QUOTA >", 0).count()
    if havegift > 0:
        return "true"
    else:
        return "false"

def getRedemptionLocation(gift):
    selectedgift = []
    if (gift == "9"):
        gifts = Gift.all().filter("GIFTID >", 8)
    else:
        gifts = Gift.all().filter("GIFTID =", int(gift))
    for i in range(0,gifts.count()) :
        selectedgift.append({"giftid": gifts[i].GIFTID, "brand": gifts[i].BRAND, "quota":int(gifts[i].QUOTA) - int(User.all().filter("OPTION = ",str(gifts[i].GIFTID)).count()),"name":gifts[i].NAME,"location": gifts[i].LOCATION})
    return selectedgift

def checkGift(date):
    all_slot = []
    gifts = Gift.query(Gift.DATE == date).fetch()
    for i in range(0,len(gifts)) :
        all_slot.append({"Giftid": gifts[i].GIFTID, "Date": gifts[i].DATE,"name":gifts[i].NAME, "quota":int(gifts[i].QUOTA) - len(Winner.query(Winner.OPTION == str(gifts[i].NAME)).fetch()) })
        # all_slot.append({"Giftid": gifts[i].GIFTID, "Date": gifts[i].DATE,"name":gifts[i].NAME, "quota":int(gifts[i].QUOTA)})
    return all_slot

def sendemail(email_data):
        # print 'test'
        # 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
        # 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
        SENDGRID_API_KEY = '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'
        SENDGRID_SENDER = 'nextmobilemarketing@nextdigital.com.hk'
        sg = sendgrid.SendGridAPIClient(SENDGRID_API_KEY)
        to_email = mail.Email(email_data[0])
        from_email = mail.Email(SENDGRID_SENDER)
        subject = 'Confirmation of 摘蘋果攞Coupon'
        emailcontent_txt1 = """
        Dear """ + email_data[1] + """  from """+ email_data[2] + """
        Thanks for joining the interactive game of 摘蘋果攞Coupon.
        Congratulation, you've won $""" + email_data[3] + """ YATA Cash coupon.
        We will send you the prize by mail soon.
        Cheers,
        Apple Daily Digital
        """
        emailcontent_html1 = """
        <html><head></head><body>
        <p>Dear """+ email_data[1] + """  from """+ email_data[2] + """</p>
        <p>Thanks for joining the interactive game of 摘蘋果攞Coupon</p>
        <p>Congratulation, you've won $"""+ email_data[3] + """ YATA Cash coupon.</p>
        <p>We will send you the prize by mail soon.</p>
        <p></p>
        <p>Cheers,<br />
        Apple Daily Digital</p>
        </body></html>
        """
        content_text = mail.Content('text/plain', "")
        content_html = mail.Content('text/html', "")
        content_text = mail.Content('text/plain', emailcontent_txt1)
        content_html = mail.Content('text/html', emailcontent_html1)
        message = mail.Mail(from_email, subject, to_email, content_html)
        message.add_content(content_text)
        response = sg.client.mail.send.post(request_body=message.get())
        print "email sent to " + email_data[0] + " " + email_data[1] + " " + email_data[2]  + " " + email_data[3]

class Counter(ndb.Model):
    COUNTER_NAME = ndb.StringProperty(default='')
    INDEX = ndb.IntegerProperty(default=0)

class Gift(ndb.Model):
    GIFTID =  ndb.IntegerProperty(default=0)
    DATE = ndb.StringProperty(default='')
    NAME = ndb.StringProperty(default='')
    QUOTA = ndb.IntegerProperty(default=0)

class User(ndb.Model):
    DATE_ADDED = ndb.DateTimeProperty(auto_now_add=True)
    DATE_MODIFIED = ndb.DateTimeProperty(auto_now=True)
    EMAIL = ndb.StringProperty(default='')

class Winner(ndb.Model):
    DATE_ADDED = ndb.DateTimeProperty(auto_now_add=True)
    DATE_MODIFIED = ndb.DateTimeProperty(auto_now=True)
    NAME = ndb.StringProperty(default='')
    COMPANY = ndb.StringProperty(default='')
    EMAIL = ndb.StringProperty(default='')
    OPTION = ndb.StringProperty(default='')

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.getLowestscore()
    def post(self):
        self.getLowestscore()
    def getLowestscore(self):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.out.write( json.dumps(checkGift('20210303')))

class getResultHandler(webapp2.RequestHandler):
    def get(self):
        self.getLowestscore()
    def post(self):
        self.getLowestscore()
    def getLowestscore(self):
        self.response.headers['Content-Type'] = 'application/csv'
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        playdate = self.request.get('pd')
        Users = User.query(User.PLAYTIME == playdate).order(User.RESULT).fetch()
        if (Users):
            # with open(playdate+'.csv', 'wb') as f:
                w = csv.writer(self.response.out,delimiter=',')
                for user in Users:
                    hkdatetime = user.DATE_ADDED + datetime.timedelta(hours=8)
                    w.writerow([hkdatetime, user.EMAIL.encode("utf-8"), user.FIRSTNAME.encode("utf-8"), user.LASTNAME.encode("utf-8"), user.PHONE.encode("utf-8"), user.PLAYTIME, user.PROMOTION, user.PROMOTION2, user.RESULT, user.SEX.encode("utf-8")])
        else:
            self.response.out.write("no users")

class QuotaHandler(webapp2.RequestHandler):
    def get(self):
        self.getquota()
    def post(self):
        self.getquota()
    def getquota(self):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        return_data = {}
        try :
            quota = checkGift('20210303')
            return_data['data'] = quota
            return_data['status'] = 'SUCCESS'
        except Exception, e:
            return_data['status'] = 'FAIL'
        self.response.out.write(json.dumps(return_data))

class checkEmailHandler(webapp2.RequestHandler):
    def get(self):
        self.checkEmail()
    def post(self):
        self.checkEmail()
    def checkEmail(self):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        pemail = self.request.get('email')
        return_data = {}
        try :
          if(checkEmailDuplication(pemail)):
            return_data['status'] = 'DULIPICATE'
          else:
            return_data['status'] = "SUCCESS"
        except Exception, e:
            return_data['status'] = 'FAIL'
        self.response.out.write(json.dumps(return_data))

class SubmitHandler(webapp2.RequestHandler):
    def get(self):
        pname = self.request.get('name')
        pcompany = self.request.get('company')
        pemail = self.request.get('email')
        poption = self.request.get('option')
    def post(self):
        self.submit()
    def submit(self):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        pname = self.request.get('name')
        pcompany = self.request.get('company')
        pemail = self.request.get('email')
        poption = self.request.get('option')
        keyname = pemail
        return_data = {}

        # print pfirstname,plastname, psex, pphone, pemail,ptime,presult,ppromotion, ppromotion2
        try:
            status = self.retreatDataAndSave(pemail,EMAIL=pemail,NAME=pname,COMPANY=pcompany,OPTION=poption)
            print status
            if status ==  "got old item" :
                # logging.info(status)
                return_data['status'] = 'REGISTER-FAIL'
                return_data['detail'] = '電話重覆登記，未能成功提交！'
            else :
                # logging.info(users)
                email_data = [pemail.encode('utf-8'),pname.encode('utf-8'),pcompany.encode('utf-8'),poption.encode('utf-8')]
                logging.info(email_data)
                # sendemail(email_data)
                return_data['status'] = 'FAIL'
                return_data['detail'] = '提交失敗！'
        except:
            logging.info('FAIL')
            return_data['status'] = 'FAIL'
            return_data['detail'] = '提交失敗！'
        self.response.out.write(json.dumps(return_data))

    def retreatDataAndSave(self,pemail,**kwds):
        currentIndex = getCurrentCount()
        try:
            result = addCounterAndSave(currentIndex,**kwds)
            return result
        except :
            return "FAIL"
        # save_status = addCounterAndSave(currentIndex,**kwds)
        # if save_status == "SUCCESS" :
        #     #sendsms(str(pphone),0)
        #     return "create new item"
        # else :
        #     print "RETRY"
        #     return self.retreatDataAndSave(pemail,pphone,**kwds)


class SubmitUserHandler(webapp2.RequestHandler):
    def get(self):
        self.submit()
    def post(self):
        self.submit()
    def submit(self):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        pemail = self.request.get('email')
        keyname = pemail
        return_data = {}
        email_data = {}
        try:
            status = self.addUser(pemail,EMAIL=pemail)
            return_data['status'] = 'SUCCESS'
            return_data['detail'] = '您已成功提交！'
        except:
            logging.info('FAIL')
            return_data['status'] = 'FAIL'
            return_data['detail'] = '提交失敗！'
        self.response.out.write(json.dumps(return_data))

    def addUser(self,pemail,**kwds):
        try:
            result = User(**kwds).put()
            return result
        except :
            return "FAIL"

class SetGiftHandler(webapp2.RequestHandler):
    def get(self):
        responsetext = ""
        scope = ['https://www.googleapis.com/auth/spreadsheets.readonly']
        credentials = ServiceAccountCredentials.from_json_keyfile_name('roadshow-game-1e6aeb6049d9.json', scope)
        gc = gspread.authorize(credentials)
        sht = gc.open_by_key('1wSIp-JaOrnJOT69ZHhKB-bh5BSfnqHmaGG9MIg2S8bw')
        worksheet = sht.worksheet("Sheet1")
        values_list = worksheet.get_all_values()
        for index in range(1,len(values_list)) :
            Gift(
                id = int(values_list[index][0]),
                GIFTID=int(values_list[index][0]),
                QUOTA=int(values_list[index][3]),
                DATE=values_list[index][1] ,
                NAME=values_list[index][2]
                ).put()
            responsetext += values_list[index][2] + '<br>'
        #wks = gc.open("Appengine test spreadsheet").sheet1
        self.response.out.write(responsetext)

class ShowResultHandler(webapp2.RequestHandler):
    def get(self):
        ppassword = self.request.get('password')
        if ppassword == "1234" :
            users = User.query().order(User.DATE_ADDED).fetch()
            winners = Winner.query().order(Winner.DATE_ADDED).fetch()
            template_values = {
                'users': users,
                'winners': winners
            }
            template = JINJA_ENVIRONMENT.get_template('admin.html')
            self.response.write(template.render(template_values))
        else:
            template = JINJA_ENVIRONMENT.get_template('login.html')
            self.response.write(template.render())

class sendWinnerEmailHandler(webapp2.RequestHandler):
    def get(self):
        self.readcsv()
    def post(self):
        self.readcsv()
    def readcsv(self):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        winnerdate = self.request.get('d')
        print winnerdate
        if winnerdate != "":
            emilcount = self.getCSVLineNumber(winnerdate)
            print "emilcount=" + str(emilcount)
            for x in range(emilcount):
                emaildata = self.getCSV(winnerdate,x)
                print(emaildata)
                self.sendemail(emaildata)
            self.response.write(emaildata)
        else:
            self.response.write('date')
    def getCSVLineNumber(self, winnerdate):
        with open(winnerdate+'.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            lastline = 0
            for row in csv_reader:
                lastline = lastline + 1
        return lastline
    def getCSV(self, winnerdate,line):
        with open(winnerdate +'.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == line:
                    print(str(line) + " " + row[0] +' won the game and winner email with qr code '+ row[1])
                    return row
                else:
                    line_count += 1


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/quota', QuotaHandler),
    ('/checkemail', checkEmailHandler),
    ('/getresult', getResultHandler),
    ('/setgift', SetGiftHandler),
    ('/showresult', ShowResultHandler),
    ('/sendwinneremail', sendWinnerEmailHandler),

], debug=True)
