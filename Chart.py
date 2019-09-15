import warnings
import itertools
import numpy as np
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")
#plt.style.use('fivethirtyeight')
import pandas as pd
import statsmodels.api as sm
import matplotlib
import json
import requests
import numpy as np
from datetime import datetime
matplotlib.rcParams['axes.labelsize'] = 14
matplotlib.rcParams['xtick.labelsize'] = 12
matplotlib.rcParams['ytick.labelsize'] = 12
matplotlib.rcParams['text.color'] = 'k'

'''
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
'''
c_id = 'd7b518ac-b11d-4e18-9ace-6c24342a7c6b'


#looks at first customer in the list
#cur_id = customer_ids[0]

accounts = requests.get('https://api.td-davinci.com/api/customers/{}/accounts'.format(c_id),
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

accid = account['bankAccounts'][1]['id']
print(accid)

# Get transaction data
trans = requests.get('https://api.td-davinci.com/api/customers/{}/transactions'.format(c_id),
    headers = { 'Authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJDQlAiLCJ0ZWFtX2lkIjoiMDAxZTI4YzAtYmVhMi0zODUwLTgxMTQtYWVkMmQ5YTU2YTlmIiwiZXhwIjo5MjIzMzcyMDM2ODU0Nzc1LCJhcHBfaWQiOiIxNDZiZDRmOS1lOWNiLTQ2M2EtOGNiZC01ZDg2MGYzZWZiNjAifQ.d7r4SbvmbRoSw43ejFqiO9K0xpBK2jpp4XPfjvAla58'})
trans_data = trans.json()

transactions = trans_data['result']

#list to hold clean transactions
trans_clean = []

keys_list = ['description', 'type', 'currencyAmount', 'originationDateTime', 'customerId', 'id', 'accountId', 'categoryTags']
for trans in transactions:
	if trans['accountId'] == accid:
		curr_trans = {}
		for key in keys_list:
			curr_trans[key] = trans[key]
		trans_clean.append(curr_trans)

trans_clean.sort( key = lambda date: datetime.strptime(date['originationDateTime'][:18], '%Y-%m-%dT%H:%M:%S')) 

for trans in reversed(trans_clean):
	trans['balance'] = card_balances[trans['accountId']] - trans['currencyAmount']
	card_balances[trans['accountId']] = trans['balance']

print trans_clean[:5]
dates = []
balances = []
for tran in trans_clean:
	balance = tran['balance']
	date = tran['originationDateTime']
	balances.append(balance)
	dates.append(pd.to_datetime(date))

plt.plot(dates, balances)
plt.ylabel('Account Balance ($)')
plt.xlabel('Date')
plt.show()

p = d = q = range(0, 2)
pdq = list(itertools.product(p, d, q))
seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]

mod = sm.tsa.statespace.SARIMAX(balances,
                                order=(1,0,0),
                                seasonal_order=(0, 1, 0, 12),
                                enforce_stationarity=False,
                                enforce_invertibility=False)
results = mod.fit()
print(results.summary().tables[1])

results.plot_diagnostics()
plt.show()
