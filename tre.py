import re
#with open('htmlPage.html', 'r') as doc:
#    doc = doc.read()
#co = re.compile('<a href="member.php?id=\d+" class="ui-profile-popup" data-user_id="\d+" data-profile_img="(([\w-]+://?|www[.])[^\s()<>]+(?:\([\w\d]+\)|([^[:punct:]\s]|/)))" data-user_name="\w+">\w+</a>')
#co = re.compile(r'<a href="member.php\?id=\d+" class="ui-profile-popup" data-user_id="\d+" data-profile_img=.*?<br><span>')
#match = co.findall(doc)

data = 'asdf:http://www.baidu.com.jpg v2ex'
#co = re.compile(r'(([\w-]+://?|www[.])[^\s()<>]+(?:\([\w\d]+\)|([^[:punct:]\s]|/)))')

co = re.compile(r'(([\w-]+://?|www[.]))[^\s()<>]+(?:([\w\d]+))')
match = co.search(data)
print (match)
