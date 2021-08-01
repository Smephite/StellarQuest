from requests.models import Response
from stellar_sdk import Server, Keypair, TransactionBuilder, Network, keypair
import os, sys, base64, requests, json

from stellar_sdk.signer import Signer
from stellar_sdk.transaction import Transaction
from stellar_sdk.transaction_envelope import TransactionEnvelope
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import friendbot

server = Server("https://horizon-testnet.stellar.org")
keypair = Keypair.from_secret(input("Enter the secret key..."))
pub_key = keypair.public_key

friendbot.fund_account(pub_key)
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
    exit("!=200 on jwt")
jwt = json.loads(resp.content)['token']

print(jwt)


data = jwt

tx = TransactionBuilder(
    source_account=acc,
    network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
    base_fee=2000
)

index = 0
while data != '':
    name = str(index).zfill(2) + data[:62]
    value = data[62:126]
    data = data[126:]
    index+=1
    tx = tx.append_manage_data_op(
        data_name=name,
        data_value=value
    )
    print(name + ":" + value)

tx = tx.build()
tx.sign(keypair)

print(server.submit_transaction(tx))