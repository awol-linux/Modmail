tickets = { 'uid': {'count': 2, 'author': 'AWOL#2301', 'channel': 797955013234262057, 'TicketNumber': 1, 'TicketName': 'ticket-1', '1': {'content': 'test', 'author': 'AWOL#2301'}, '2': {'content': 'test', 'author': 'AWOL#2301'}}}
from pymongo import MongoClient
USER = 'root'
PASS = 'rootpassword'
# Create connection to MongoDB
client = MongoClient('172.20.0.10', 27017 , username=USER, password=PASS)
db = client['tickets']
collection = db['723183706054983721']

# Build a basic dictionary

# Insert the dictionary into Mongo
collection.insert_one(tickets['uid'])
print(db.list_collection_names())
#collection.update_one({"count" : {}}, { '$inc': { 'count': 1 }})
#counts = collection.find({ "$field" : "count" })
#for x in counts:
#    print(x)
db.list_collection_names()
for db in client.list_databases():
    print(db)





#print(db.count())
