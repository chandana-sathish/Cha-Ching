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
cur_id = customer_ids[0]
#cur_id = 'd7b518ac-b11d-4e18-9ace-6c24342a7c6b' - tommy cherny

accounts = requests.get('https://api.td-davinci.com/api/customers/{}/accounts'.format(cur_id),
    headers = { 'Authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJDQlAiLCJ0ZWFtX2lkIjoiMDAxZTI4YzAtYmVhMi0zODUwLTgxMTQtYWVkMmQ5YTU2YTlmIiwiZXhwIjo5MjIzMzcyMDM2ODU0Nzc1LCJhcHBfaWQiOiIxNDZiZDRmOS1lOWNiLTQ2M2EtOGNiZC01ZDg2MGYzZWZiNjAifQ.d7r4SbvmbRoSw43ejFqiO9K0xpBK2jpp4XPfjvAla58'})
acc_data = accounts.json()

#print(acc_data.keys())
account = acc_data['result']
# print(acc_data['result'])

# get balance (will have to change to accomodate for savings, chequing, and credit card)
card_balances = {}
for card in account['bankAccounts']:
	card_balances[card['id']] = card['balance']

for card in account['creditCardAccounts']:
	card_balances[card['id']] = card['balance']


# Get transaction data
trans = requests.get('https://api.td-davinci.com/api/customers/{}/transactions'.format(cur_id),
    headers = { 'Authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJDQlAiLCJ0ZWFtX2lkIjoiMDAxZTI4YzAtYmVhMi0zODUwLTgxMTQtYWVkMmQ5YTU2YTlmIiwiZXhwIjo5MjIzMzcyMDM2ODU0Nzc1LCJhcHBfaWQiOiIxNDZiZDRmOS1lOWNiLTQ2M2EtOGNiZC01ZDg2MGYzZWZiNjAifQ.d7r4SbvmbRoSw43ejFqiO9K0xpBK2jpp4XPfjvAla58'})
trans_data = trans.json()

transactions = trans_data['result']

#list to hold clean transactions
trans_clean = []
categoryTagsList = []

keys_list = ['description', 'type', 'currencyAmount', 'originationDateTime', 'customerId', 'id', 'accountId', 'categoryTags']
for trans in transactions:
	curr_trans = {}
	for key in keys_list:
<<<<<<< HEAD
		temp_info[key] = trans[key]
	trans_clean.append(temp_info)

with open("transaction.json", "w+") as f:
	f.truncate(0)
	f.write(json.dumps(trans_clean, sort_keys=True, indent=4))

#for i in trans_clean:
#	f.write(json.dumps(i))
=======
		curr_trans[key] = trans[key]

	# if trans['type'] == 'DepositAccountTransaction':
	curr_trans['balance'] = card_balances[card['id']] + trans['currencyAmount']
	# else: # credit card
	# 	curr_trans['balance'] = card_balances[card['id']] - trans[]
	trans_clean.append(curr_trans)


f = open('transactionbalance.txt', 'w+')
for i in trans_clean:
	f.write(json.dumps(i))
>>>>>>> 676a99c7d915eaf7e1fec3914a0c2bec603f4c8f

# print(temp_info)
f.close()
# numTransactions = 1
# numCategoryTags = 1
# a = np.zeros(shape = (numTransactions, numCategoryTags))
# # a = np.array(trans_clean)
# print(a)










