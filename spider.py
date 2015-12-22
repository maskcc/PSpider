import urllib.request
import urllib.parse
import login
import re

class User(object):
    def __init__(self, ID, descript, imgSrc):
        self.__ID = ID
        self.__des = descript
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

Login = login.login('pickmio', 'jxp2580')
header = login.HttpHeadBuilder().mockHeader
url = 'http://www.pixiv.net/bookmark.php?type=user'
request = urllib.request.Request(url, headers = header)
request.add_header('Cookie', Login.cookie)
rsp = urllib.request.urlopen(request)
print(rsp.code)
htmlPage = rsp.read()
htmlPage = htmlPage.decode('utf-8')
htmlPage = htmlPage.replace('\r\n', ' ')
with open('htmlPage.html', 'w') as f:
    f.write(htmlPage)
#pattern = re.compile(r'(?<=<ul class="user-list"><li><a href="/member.php\?id=)\d+')
pattern = re.compile(r'<div class="userdata"><a href="member.php\?id=\d+" class="ui-profile-popup" data-user_id="\d+" data-profile_img=.*?(?=<br><span>)')
match = pattern.findall(htmlPage)
users = []
i = 0
print(len(match))
if match:
    for keys in match:
        users.append(parseUser(keys))

for v in users:
    request = urllib.request.Request(v.imgSrc, headers = header)
    request.add_header('Cookie', Login.cookie)
    rsp = urllib.request.urlopen(request)
    img = rsp.read()
    imgfile = open(r'./file/' + v.ID + '.' + v.imgSrc.split('.')[-1], 'wb+')
    imgfile.write(img)

