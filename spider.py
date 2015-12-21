import urllib.request
import urllib.parse
import login
import re

class User(object):
    def __init__(self, ID, descript, imgSrc):
        self.__ID = ID
        self.__des = descript
        self.imgSrc = imgSrc

    @property
    def ID(self):
        return self.__ID

    @property
    def des(self):
        return self.__des

    @property
    def imgSrc(self):
        return self.__imgSrc

    
def parseUser(info):
    pattern = re.compile('(?<=member.php\?id=)\d+')
    match = pattern.search(info)
    print (match.group())
        

Login = login.login('pickmio', 'jxp2580')
header = login.HttpHeadBuilder().mockHeader
url = 'http://www.pixiv.net/bookmark.php?type=user'
request = urllib.request.Request(url, headers = header)
request.add_header('Cookie', Login.cookie)
rsp = urllib.request.urlopen(request)
print(rsp.code)
htmlPage = rsp.read()
htmlPage = htmlPage.decode('utf-8')
with open('htmlPage.html', 'w') as f:
    f.write(htmlPage)
#pattern = re.compile(r'(?<=<ul class="user-list"><li><a href="/member.php\?id=)\d+')
pattern = re.compile(r'<a href="member.php\?id=\d+" class="ui-profile-popup" data-user_id="\d+" data-profile_img=.*?<br><span>')
match = pattern.findall(htmlPage)

if match:
    for keys in match:
        parseUser(keys) 
