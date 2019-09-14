# install the requests package using 'pip3 install requests'
import requests
import json
import numpy as np

response = requests.post('https://api.td-davinci.com/api/raw-customer-data',
    headers = { 'Authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJDQlAiLCJ0ZWFtX2lkIjoiMDAxZTI4YzAtYmVhMi0zODUwLTgxMTQtYWVkMmQ5YTU2YTlmIiwiZXhwIjo5MjIzMzcyMDM2ODU0Nzc1LCJhcHBfaWQiOiIxNDZiZDRmOS1lOWNiLTQ2M2EtOGNiZC01ZDg2MGYzZWZiNjAifQ.d7r4SbvmbRoSw43ejFqiO9K0xpBK2jpp4XPfjvAla58', "continuationToken": "CONTINUATION TOKEN" })
response_data = response.json()

request_id = response_data["requestId"]

customer_data = response_data["result"]["customers"]
# team id: 146bd4f9-e9cb-463a-8cbd-5d860f3efb60

customer_ids = []
for customer in customer_data:
	customer_ids.append(customer["id"])
	#print(customer["id"])

#print(customer_ids)

customer_transactions = []

#looks at first customer in the list
categoryTagsList = []

for i in range(100):
	cur_id = customer_ids[i]

	trans = requests.get('https://api.td-davinci.com/api/customers/{}/transactions'.format(cur_id),
	    headers = { 'Authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJDQlAiLCJ0ZWFtX2lkIjoiMDAxZTI4YzAtYmVhMi0zODUwLTgxMTQtYWVkMmQ5YTU2YTlmIiwiZXhwIjo5MjIzMzcyMDM2ODU0Nzc1LCJhcHBfaWQiOiIxNDZiZDRmOS1lOWNiLTQ2M2EtOGNiZC01ZDg2MGYzZWZiNjAifQ.d7r4SbvmbRoSw43ejFqiO9K0xpBK2jpp4XPfjvAla58'})
	trans_data = trans.json()

	transactions = trans_data['result']

	keys_list = ['description', 'type', 'currencyAmount', 'originationDateTime', 'customerId', 'id', 'accountId', 'categoryTags']
	for trans in transactions:
		if (trans['categoryTags'] not in categoryTagsList):
			categoryTagsList.append(trans['categoryTags'])

print(categoryTagsList)
print(categoryTagsList.length())

