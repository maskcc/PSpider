import urllib.request
import urllib.parse
import login
import re
import DBInstance as DB
import requests
# I have to add exception to the operation of openning one page!
# And also have to set the frequency to open one page! so that it can not catch me
# I also have to add the judgement that when is timeout , drop the web access
# Need to change the cookie when it does not work
# Need to update the database when a special time passed!
MainPage = 'http://www.pixiv.net/member_illust.php?id='
ImgPage = 'http://www.pixiv.net/member_illust.php?mode=medium&illust_id='
MangaPage = 'http://www.pixiv.net/member_illust.php?mode=manga&illust_id='

class User(object):
    def __init__(self, ID, name,  description, imgSrc):
        self.__ID = ID
        self.__name = name
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

    @property
    def name(self):
        return self.__name

    def show(self):
        print('ID:', self.__ID)
        print('name', self.__name)
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
    return User(ID, name, des, imgSrc)

class UserParse(object):
    def __init__(self, name, cookie):
        self.__cookie = cookie
        self.__Users = []
        self.opener = {}
        self.set_opener()
        self._name = name

        self.__maxCount = 0
        self.__firstUrl = 'http://www.pixiv.net/bookmark.php?type=user'
        self.__firstPage = ''
        self.__urlPages = []
        self.set_page_urls()
        self.parse_all_pages()
        self._db = DB.DBInstance()
        self.add_2_db()

    # I can only get 10 pages on the main page, perhaps I need to try until the code is not 200
    def set_page_urls(self):
        self.__firstPage = self.opener.open(self.__firstUrl).read()
        self.__firstPage = self.decode_page(self.__firstPage)
#        pattern = re.compile(r'(?<=<a href="bookmark.php\?type=user&amp;rest=show&amp;p=)\d+')
#        rsp = pattern.findall(self.__firstPage)
#        rsp = [int(x) for x in rsp if x]
#        self.__maxCount = max(rsp)
        self.__maxCount = 12 # here need to change when you are running
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
        ids = []
        for v in self.__Users:
            if self.__Users:
                self._db.add_author(v.ID, v.name, v.des, v.imgSrc)
                ids.append(v.ID)
        self._db.add_my_drawer(self._name, ids)

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
class ImagePraser(object):
    def __init__(self, userName, pwd):
        self._DB = DB.DBInstance()
        self._userName = userName
        self._pwd = pwd
        self._cookie = self._DB.get_cookie(userName, pwd)
        print('cookie:', self._cookie)
        if not self._cookie:
            print('please parse image after login!')
            return
        self.opener = {}
        self.set_opener()

    def set_opener(self):        
        urllib.request.socket.setdefaulttimeout(10)
        self.opener = urllib.request.build_opener()    
        self.opener.addheaders = login.HttpHeadBuilder().arrHeader
        self.opener.addheaders.append(('Cookie', self._cookie))

    def hasNext(self, page): # to judge if there is next page
        pattern = re.compile('下一页')  
        match = pattern.search(page)
        if match:
            return True
        return False

    def parse_image_id(self):
         data = self._DB.get_my_drawer(self._userName)
         for v in data:
             for i in range(1000):
                 url = MainPage + str(v) + '&type=all&p=' + str(i + 1)
                 print('authorPage is:',  url)
                 rst =  self.opener.open(url)
                 print('return code is:', rst.code)
                 rst = rst.read()
                 rst = rst.decode('utf-8')
                 if not self.hasNext(rst):
                     print('can not find any more')
                     break
                 self.parse_image_url(rst)

    def parse_image_url(self, page):
        pattern = re.compile('(?<=a href="/member_illust.php\?mode=medium&amp;illust_id=)\d+')
        match = pattern.findall(page)
        i = 1
        if not match:
            print('match nothing')
            return
        for v in match:
               sourceUrl = ImgPage + str(v)
               page = self.opener.open(sourceUrl)
               page = page.read()
               page = page.decode('utf-8')
               f =  open('data.html', 'w')
               f.write(page)
               pattern = re.compile('(?<=data-src=").* (?=class="original-image")') 
               imgurl = pattern.search(page).group()
               imgurl = imgurl.split('"')[0]
               print(str(i) + '.downloading url:', imgurl)
               self.opener.addheaders.append(('Referer', sourceUrl))  # add reference ,with out this will return 404
               img = self.opener.open(imgurl).read()
               i = i + 1 
               self.opener.addheaders.pop() # push the last Reffering and replace it 
               with open((str(v) + '.' + imgurl.split('.')[-1]), 'wb') as f:
                   f.write(img)
                   f.close()
               




UserParse('pickmio', login.login('pickmio', 'jxp2580').cookie)
p = ImagePraser('pickmio', 'jxp2580')
p.parse_image_id()
















