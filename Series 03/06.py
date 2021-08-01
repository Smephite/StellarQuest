from requests.models import Response
from stellar_sdk import Server, Keypair, TransactionBuilder, Network, keypair
import os, sys, requests, hashlib, base64

from stellar_sdk.signer import Signer
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import friendbot

server = Server("https://horizon-testnet.stellar.org")

png = requests.get("https://cdn.discordapp.com/attachments/765215066420805663/845133032443740160/GCEE5H3RI2MFP4UQ4NHFKLGTIHILWA775AM7KTLU5HUBSLOBJN7M4RSL.png", stream=True)

if png.status_code != 200:
    exit

keypair = Keypair.from_secret(input("Enter the secret key..."))
pub_key = keypair.public_key


friendbot.fund_account(pub_key)
acc = server.load_account(keypair)
tx = TransactionBuilder(
    source_account=acc,
    network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
    base_fee=2000
)

png = png

data = base64.encodebytes(png.content).replace(b'\n', b'')


index = 0
while data != b'':
    name = str(index).zfill(2) + data[:62].decode('ascii')
    value = data[62:126]
    data = data[126:]
    index+=1
    tx = tx.append_manage_data_op(
        data_name=name,
        data_value=value
    )

tx = tx.build()
tx.sign(keypair)

print(server.submit_transaction(tx))



