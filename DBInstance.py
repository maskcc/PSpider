from pymongo import MongoClient
import pymongo

class DBInstance(object):
    def __init__(self):
        # connet to the db and create collections
        self._client = MongoClient()
        self._db = self._client.spider   #the data base named spider
        self._authors = self._db.authors #the drawers' info stored in _authors
        self._users = self._db.users     #the info about who login
        self._authors.create_index([('ID', pymongo.ASCENDING)], unique=True)
        self._users.create_index([('name', pymongo.ASCENDING)], unique=True)

    def add_author(self, ID, des, imgSrc):
        try:
            self._authors.insert({'ID': ID, 'des': des, 'imgSrc': imgSrc})
        except pymongo.errors.DuplicateKeyError:
            print(ID, ' is already on the db')

    def get_author(self, ID):
        rst = self._authors.find_one({'ID': ID})
        if not rst:
            print('the user\'s ID is not in the db')
            return None
        return rst.ID, rst.des, rst.imgSrc       
    # name: the user name he login, pwd: the password, cookie: tmp cookie get, alist: the users he followed with intrest

    def add_user(self, name, pwd):
        try:
            self._users.insert({'name': name, 'pwd': pwd})
        except pymongo.errors.DuplicateKeyError:
            print(name, ' you hava logined in our system!')

    # the user id is needed to transfer to string, number in db are stored in float whith a '0' end
    def add_my_drawer(self, name, IDList):
        my = self._users.find_one({'name': name})
        if not my:
            print('add my drawer fail, name is wrong!')
            return False
        self._users.update({'name': name}, {'$set': {'IDList': IDList}})
        # here may have memory leak???
        
    def get_cookie(self, name, pwd):
        user = self._users.find_one({'name': name, 'pwd' : pwd})
        cookie = ''
        try:
            cookie = user['cookie']
        except KeyError:
            print('user name or password is not right! please try agin!')
            return None
        except TypeError:
            print('user name or password is not right! please try agin!')
            return None
        return cookie

    def update_cookie(self, name, cookie):
        user = self._users.find_one({'name': name})
        if not user:
            print('can not find the user')
            return False
        self._users.update({'name': name}, {'$set': {'cookie': cookie}})
        return True
