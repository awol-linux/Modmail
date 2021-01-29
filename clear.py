from pymongo import MongoClient
import os

PASS = os.getenv('MONGO_PASSWORD')
USER = os.getenv('MONGO_USER')

# Create connection to MongoDB
client = MongoClient('172.20.0.10', 27017 , username=USER, password=PASS)
ticket_first = client['tickets']
uid = client['userid']
setting = client['settingdb']

client.drop_database(ticket_first)
client.drop_database(uid)
client.drop_database(setting)
