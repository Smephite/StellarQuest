from requests.models import Response
from stellar_sdk import Server, Keypair, TransactionBuilder, Network, keypair
import os, sys, base64, requests, json
from stellar_sdk.asset import Asset

from stellar_sdk.signer import Signer
from stellar_sdk.transaction import Transaction
from stellar_sdk.transaction_envelope import TransactionEnvelope
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import friendbot

server = Server("https://horizon-testnet.stellar.org")
keypair = Keypair.from_secret(input("Enter the secret key..."))
pub_key = keypair.public_key
#friendbot.fund_account(pub_key)
acc = server.load_account(keypair)
endpoint = "https://testanchor.stellar.org/auth"

challenge = requests.get(endpoint+f'?format=json&account={pub_key}')

if challenge.status_code != 200:
    exit("!=200 on challenge")
challenge = challenge.content
challenge = json.loads(challenge)
print(challenge)
tx = TransactionEnvelope.from_xdr(challenge['transaction'], network_passphrase=challenge['network_passphrase'])
if tx.transaction.sequence != 0:
    exit("Invalid seq number!")
tx.sign(keypair)

print(tx.to_xdr())

resp = requests.post(endpoint, json={"transaction": tx.to_xdr()})
if resp.status_code != 200:
    exit(f"!=200 on jwt {resp.status_code} {resp.content}")
jwt = json.loads(resp.content)['token']

asset = Asset('MULT', 'GDLD3SOLYJTBEAK5IU4LDS44UMBND262IXPJB3LDHXOZ3S2QQRD5FSMM')

tx = TransactionBuilder(
    source_account=acc,
    network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
    base_fee=2000
).append_change_trust_op(
    asset_code=asset.code,
    asset_issuer=asset.issuer
).build()

tx.sign(keypair)
print(server.submit_transaction(tx))

sep_6_endpoint = 'https://testanchor.stellar.org/sep6'
kyc_endpoint = 'https://testanchor.stellar.org/kyc'
hed = {'Authorization': 'Bearer ' + jwt}

add_kyc = requests.put(f"{kyc_endpoint}/customer", headers=hed, json={
    "first_name": "My",
    "last_name": "Cool",
    "email_address": "Test",
    "bank_number": "00000",
    "bank_account_number": "0000",
    "account": pub_key
})

print(add_kyc.content)

deposit = requests.get(f"{sep_6_endpoint}/deposit?asset_code=MULT&account={pub_key}&type=bank_account&amount=10", headers=hed)
print(deposit.content)