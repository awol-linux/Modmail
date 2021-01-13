import etcd
client = etcd.Client(host='172.20.0.10', port=2379)

ticket = { 'uid': {'count': 2, 'author': 'AWOL#2301', 'channel': 797955013234262057, 'TicketNumber': 1, 'TicketName': 'ticket-1', 1: {'content': 'test', 'author': 'AWOL#2301'}, 2: {'content': 'test', 'author': 'AWOL#2301'}}}
print(type(ticket))
client.get('/version')
def make_etcd(search_dict):
    """
    Takes a dict with nested lists and dicts and converts it to fs for etcd
    """
    fields_found = []

    for key, value in search_dict.items():

        fields_found.append(key)
        if isinstance(value, dict):
            results = make_etcd(value)
            for result in results:
                if result is not None:
                    fields_found.append(str(key) + '/' + str(result))

        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    more_results = make_etcd(value)
                    for another_result in more_results:
                        fields_found.append(str(key) + '/' + str(another_result))
    return fields_found
for url in make_etcd(ticket):
   print('/' + url)
