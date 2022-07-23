from pprint import pprint
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
db = client['insta_com']

search = 'dr_polinandreeva'
search_1 = 'marinagafonova'

for user in db.insta_com.find(
        {'sub_username': search_1, 'sub_type': 'follower'}):
    pprint(user)
for user in db.insta_com.find(
        {'sub_username': search_1, 'sub_type': 'following'}):
    pprint(user)

for user in db.insta_com.find(
        {'sub_username': search, 'sub_type': 'follower'}):
    pprint(user)
for user in db.insta_com.find(
        {'sub_username': search, 'sub_type': 'following'}):
    pprint(user)
