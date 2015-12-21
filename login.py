# -*- coding:utf-8 -*-
#! /usr/bin/python3

import urllib.request
import urllib.parse
from urllib.error import HTTPError, URLError
import http.cookiejar

def parseCookie(values):
    #print(values)
    rst = {}
    vlist = values.split(';')
    for v in vlist:
        if('' != v):
            head = v.split('=')[0]
            tail = v.split('=')[1]
            rst[head] = tail
    return rst 

class HTTPRedirectHandler(urllib.request.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        #print("Redirect is called but I get it")
        #print("msg:", msg)
        #print("headers:", headers)
        realUrl = headers.get("Location")
        cookie = headers.get_all('Set-Cookie')
        cookie1 = cookie[1] + ';' +  cookie[2]
        cookie1 = parseCookie(cookie1) 
        cookie = 'PHPSESSID=' + cookie1['PHPSESSID'] + ';'
        cookie += 'device_toke=' + cookie1['device_token']
        return cookie, realUrl  #this will return to the opener function


class HttpHeadBuilder(object):
    def __init__(self):
        self.__mockHeader = {}
        self.initHeader()

    @property
    def mockHeader(self):
        return self.__mockHeader
    
    def initHeader(self):
        self.__mockHeader = {
            "ContentType" : "application/x-www-form-urlencoded",\
            "User-Agent" : "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:35.0) Gecko/20100101 Firefox/35.0",\
            "Referer" : "https://www.secure.pixiv.net/login.php",\
            "Accept" : "test/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",\
            "Accept-Language" : "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",\
            # "Accept-Encoding" : "gzip, deflate",\    #is open this header, the server will compress the package
            "Connection" : "keep-alive",\
            #"Content-Length" : 47,\
            "Cache-Control" : "max-age=0",\
            "DNT" : "1"  
        }

class HttpPostDataBuilder(object):
    def __init__(self, postData):
            self.__postData = postData
            self.encodePostData()

    def encodePostData(self):
        self.__postData = urllib.parse.urlencode(self.postData)
        self.__postData = self.postData.encode(encoding='utf-8')
   
    @property
    def postData(self):
        return self.__postData
    

class login(object):
    def __init__(self, userName, pwd, loginPage = 'https://www.secure.pixiv.net/login.php'):
        if(str != type(userName)):               #check the paragram type
            raise ValueError("userName must be a str")
            
            if(str != type(pwd)):
                raise ValueError("pwd must be a str")

        
        try:
            with open('cookie', 'r') as cookieFile:
                self.__cookie = cookieFile.read()
        except IOError as e:
            print('can not find the cookie file, just login')
            self.__userName = userName
            self.__pwd = pwd
            self.__cookie = ""  #the cookie server returned


            t = HttpHeadBuilder()
            self.__mockHeader = t.mockHeader
            self.__postData = {}
            self.initPostData()
            self.__loginPage = loginPage

            self.makeLogin()    
            self.openMainPage()
            self.saveCookie()

    def initPostData(self):
        self.__postData["mode"] = "login"
        self.__postData["pixiv_id"] = self.__userName
        self.__postData["pass"] = self.__pwd
        self.__postData["skip"] = "1"
        
        self.__postData = HttpPostDataBuilder(self.__postData).postData
        

    def makeLogin(self):
        self.cookieJar = http.cookiejar.CookieJar()
        self.request = urllib.request.Request(url = self.__loginPage, data = self.__postData, headers = self.__mockHeader, method = 'POST')
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookieJar), HTTPRedirectHandler())
        self.__cookie,self.__loginPage = self.opener.open(self.request)

    def openMainPage(self):
        self.__mockHeader['Cookie'] = self.__cookie
        #print('header = ', self.__mockHeader)
        #print('url = ', self.__loginPage)
        self.request = urllib.request.Request(url = self.__loginPage, headers = self.__mockHeader)
        result =  self.opener.open(self.request)
        
        tmpCookie = result.info().get_all('Set-Cookie')
        cookieStr = ''
        for v in tmpCookie:
           cookieStr += v + ';'

        cookieObj = parseCookie(cookieStr)
        self.__cookie += '; module_orders_mypage=' + cookieObj['module_orders_mypage']

    def saveCookie(self):
        cookieFile = open('cookie', 'w')
        cookieFile.write(self.__cookie)
        cookieFile.close()

    @property
    def cookie(self):
        return self.__cookie   
