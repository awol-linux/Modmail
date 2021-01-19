from pymongo import MongoClient
import os

PASS = os.getenv('MONGO_PASSWORD')
USER = os.getenv('MONGO_USER')
print(USER + ' ' + PASS)
mdbclient = MongoClient('172.20.0.10', 27017, username=USER, password=PASS)
ticket_first = mdbclient['tickets']
user_first = mdbclient['userid']
RemoveID = { "addresses": { "$slice": [0, 1] } ,'_id': 0}


class search():
    def all_tickets_for_user(uid):
        #terms = { "TicketName" : {"$exists" : "true" } } 
        terms = {} 
        query = user_first[str(uid)].find(terms, RemoveID)
        ticket_names = []
        for ticketname in query:
            ticket_names.append(ticketname['TicketName']) 
        return ticket_names

    def by_user_active(uid):
        terms = {"status" : "active" } 
        query = user_first[str(uid)].find(terms, RemoveID)
        tickets = []
        for ticket in query:
            tickets.append(ticket['TicketName'])
        if len(tickets) == 1:
            return tickets[0]
        if len(tickets) == 0:
            return None

    def by_ticket(TicketName):
        terms = {}
        query = ticket_first[TicketName].find(terms, RemoveID)
        tickets = []
        for ticket in query:
            tickets.append(ticket)
        if len(tickets) == 1:
            return tickets[0]
        if len(tickets) == 0:
            return None


    def add_message(owner, TicketName, message_data):
        terms = {"uid": owner}
        push_message = {'$push': {'messages': message_data}}
        update_count = {"$inc" : { "Count" : 1}}
        ticket_first[TicketName].update_one(terms, push_message)
        ticket_first[TicketName].update_one(terms, update_count)

    def new_ticket(user_info):
        amount = len(ticket_first.list_collection_names()) + 1
        TicketName = 'ticket-' + str(amount)
        user_info['TicketName'] = TicketName
        uid = str(user_info['uid'])
        ticket_info = {"TicketName" : TicketName, "status": "active"}
        ticket_first[TicketName].insert_one(user_info)
        user_first[uid].insert_one(ticket_info)
        return TicketName

    def get_owner(TicketName):
        terms = {}
        query = ticket_first[TicketName].find(terms, RemoveID)
        tickets = []
        for ticket in query:
            tickets.append(ticket['uid'])
        if len(tickets) == 1:
            return tickets[0]
        if len(tickets) == 0:
            return None


    def get_messages_by_tickets(TicketName):
        terms = { 'author': {'$exists': 'true' }}
        query = ticket_first[TicketName].find(terms, RemoveID)
        tickets = []
        for ticket in query:
            tickets.append(ticket['messages'])
        if len(tickets) == 1:
            return tickets[0]
        if len(tickets) == 0:
            return None


    def all_messages_by_user(username):
        all_messages = []
        for ticket in ticket_first.list_collection_names():
            terms = { 'messages.author' : username }
            query = ticket_first[ticket].find(terms, RemoveID)
            for ticketname in query:
                all_messages.append(ticketname) 
        return all_messages

    def archive_channel(TicketName):
        terms = { "uid" : {"$exists" : "true" } }
        tickets = []
        for ticket in ticket_first[TicketName].find(terms, RemoveID):
            tickets.append(ticket['uid'])
        if len(tickets) == 1:
            uid = tickets[0]
            print(uid)
        new_terms = { "TicketName" : TicketName }
        new_update = { '$set': { 'status' : 'closed' } }
        user_first[str(uid)].update_one(new_terms, new_update)
