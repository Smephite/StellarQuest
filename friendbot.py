import requests

url = 'https://friendbot.stellar.org'

def fund_account(pub_key):
    resp = requests.get(url, params={'addr': pub_key})
    print(f"Funding account {pub_key}: {resp}")
