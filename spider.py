import urllib.request
import urllib.parse
import login
import re
import DBInstance as DB

class User(object):
    def __init__(self, ID, description, imgSrc):
        self.__ID = ID
        self.__des = description
        self.__imgSrc = imgSrc

    @property
    def ID(self):
        return self.__ID

    @property
    def des(self):
         return self.__des

    @property
    def imgSrc(self):
        return self.__imgSrc

    def show(self):
        print('ID:', self.__ID)
        print('imgSrc:', self.__imgSrc)
        print('descript:', self.__des)
        print('\n')


def parseUser(info):
    pattern = re.compile(r'(?<=member.php\?id=)\d+')
    match = pattern.search(info)
    ID =  match.group()
    pattern = re.compile(r'(([\w-]+://?|www[.]))[^\s()<>]+(?:([\w\d]+))')
    match = pattern.search(info)
    imgSrc = match.group()
    pattern = re.compile(r'(?<=data-user_name=").+(?=">)')
    match = pattern.search(info)
    name = match.group()
    pattern = re.compile(r'(?<=</a>).+$')
    match = pattern.search(info)
    des = match.group()
    return User(ID, des, imgSrc)

class UserParse(object):
    def __init__(self, cookie):
        self.__cookie = cookie
        self.__Users = []
        self.opener = {}
        self.set_opener()
        
        self.__maxCount = 0
        self.__firstUrl = 'http://www.pixiv.net/bookmark.php?type=user'
        self.__firstPage = ''
        self.__urlPages = []
        self.set_page_urls()
        self.parse_all_pages()
        self._db = DB.DBInstance()
        self.add_2_db()

    def set_page_urls(self):
        self.__firstPage = self.opener.open(self.__firstUrl).read()
        self.__firstPage = self.decode_page(self.__firstPage)
        pattern = re.compile(r'(?<=<a href="bookmark.php\?type=user&amp;rest=show&amp;p=)\d+')
        rsp = pattern.findall(self.__firstPage)
        rsp = [int(x) for x in rsp if x]
        self.__maxCount = max(rsp)
        for i in range(self.__maxCount):
            url = 'http://www.pixiv.net/bookmark.php?type=user&rest=show&p=' + str(i+1)
            self.__urlPages.append(url) 
  
    def decode_page(self, p):
        page = p.decode('utf-8')
        page = page.replace('\r\n', ' ')
        return page
        
    def set_opener(self):
        self.opener = urllib.request.build_opener()
        self.opener.addheaders = login.HttpHeadBuilder().arrHeader
        self.opener.addheaders.append(('Cookie', self.__cookie))

    def parse_all_pages(self):
        for v in self.__urlPages:
            html = self.opener.open(v).read()
            html = self.decode_page(html)
            self.parse_onepage(html)

    def parse_onepage(self, html):
        pattern = re.compile(r'<div class="userdata"><a href="member.php\?id=\d+" class="ui-profile-popup" data-user_id="\d+" data-profile_img=.*?(?=<br><span>)')
        match = pattern.findall(html)        
        if match:
            for v in match:
                self.__Users.append(parseUser(v))
    def add_2_db(self):
        for v in self.__Users:
            if self.__Users:
                self._db.add_author(v.ID, v.des, v.imgSrc)

    def show(self):
        print('total:', len(self.__Users))
        for v in self.__Users:
            s = v
            try:
                with open(r'./file/' + s.ID + '.' + s.imgSrc.split('.')[-1], 'r') as imgfile:
                    print('file exist:', s.ID)
            except FileNotFoundError as e:
                    rsp = self.opener.open(s.imgSrc)
                    print('downloading file...')

                    img = rsp.read()
                    imgfile = open(r'./file/' + s.ID + '.' + s.imgSrc.split('.')[-1], 'wb+')
                    imgfile.write(img)
            v.show()
'''
class ImagePraser(obejct):
    def __init__(self):
'''     
























