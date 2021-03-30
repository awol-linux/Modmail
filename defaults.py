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

settingcol.insert_many([
    { 'name' : "prefix", 'value' : "&", 'Description' : 'Sets the command prefix' }, 
    { 'name' : "category_id",  'value' : 798284727794270229, 'Description' : 'Category where the complaint channels are placed' } ,
    { 'name' : "command_channel_id" , 'value' : 797996052074201088, 'Description': 'Channel where closed tickets get logged'},
    { 'name' : "log_channel_id", 'value' : 788119131068301335, 'Description': 'Channel where search responses go' },
    { 'name' : "admin_roles", 'value' : [789329882605813760], 'Description': 'Channel where search responses go' }])

counts = settingcol.find({},{ "addresses": { "$slice": [0, 1] } ,'_id': 0})
for key in counts:
    print(key)
