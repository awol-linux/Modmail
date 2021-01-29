from pymongo import MongoClient
import os

PASS = os.getenv('MONGO_PASSWORD')
USER = os.getenv('MONGO_USER')

# Create connection to MongoDB
client = MongoClient('172.20.0.10', 27017 , username=USER, password=PASS)
setting = client['settingdb']
settingcol = setting['settings']

# Clear settings

client.drop_database(setting)

# Insert the settings into Mongo

settingcol.insert_one({ "prefix" : "&", 
    "category_id": 798284727794270229,
    "command_channel_id" : 797996052074201088,
    "log_channel_id" : 788119131068301335 })

counts = settingcol.find({},{ "addresses": { "$slice": [0, 1] } ,'_id': 0})
for key in counts:
    print(key)
