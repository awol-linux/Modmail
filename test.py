from pymongo import MongoClient
USER = 'root'
PASS = 'rootpassword'


# Create connection to MongoDB
client = MongoClient('172.20.0.10', 27017 , username=USER, password=PASS)
db = client['tickets']
uid = client['userid']
collection = db['ticket-1']
setting = client['settingdb']
settingcol = setting['settings']


# Build a basic dictionary

client.drop_database(setting)

# Insert the dictionary into Mongo

settingcol.insert_one({ 
    "prefix" : "&", 
    "catagory_id": "797996052074201088",
    "command_channel_id" : "797996052074201088"
    })

print(setting.list_collection_names())

#collection.update_one({"count" : {}}, { '$inc': { 'count': 1 }})

counts = settingcol.find({},
        { "addresses": { "$slice": [0, 1] } ,'_id': 0}
        )
for key in counts:
    print(key)

#print(db.count())
#client.drop_database(db)
#client.drop_database('tickets')
#client.drop_database('userid')
#client.drop_database('db')
