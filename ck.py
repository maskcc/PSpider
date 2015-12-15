import urllib.request

LoginPage = "http://www.pixiv.net/bookmark.php?type=user"

header_dic = {
        "ContentType" : "application/x-www-form-urlencoded",\
        "User-Agent" : "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:35.0) Gecko/20100101 Firefox/35.0",\
        "Referer" : "http://www.pixiv.net/member_illust.php?mode=medium&illust_id=8372529",\
        "Accept" : "image/png,image/*;q=0.8,*/*;q=0.5",\
        "Accept-Language" : "en-US,en;q=0.5",\
        #"Accept-Encoding" : "gzip, deflate",\
        "Connection" : "keep-alive",\
        "Cookie" : "PHPSESSID=7112855_8916413addbbd3343215929ac86265240;  device_token=75384695805b6b3ecbcafe780f74acd9; module_orders_mypage=%5B%7B%22name%22%3A%22everyone_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22spotlight%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22featured_tags%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22contests%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22following_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22mypixiv_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22booth_follow_items%22%2C%22visible%22%3Atrue%7D%5D",\
        "Cache-Control" : "max-age=0",\
        "DNT" : "1"  
}
url = urllib.request.Request(url = LoginPage, headers = header_dic)
response = urllib.request.urlopen(url)
print(response.code)
print(response.reason)
content = response.read()
print(content.decode('utf8'))
pic = open("fe.html", "wb+")
pic.write(content)
