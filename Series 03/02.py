from requests.models import Response
from stellar_sdk import Server, Keypair, TransactionBuilder, Network, keypair
import os, sys

from stellar_sdk.signer import Signer
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import friendbot

server = Server("https://horizon-testnet.stellar.org")
keypair = Keypair.from_secret(input("Enter the secret key..."))
pub_key = keypair.public_key

acc = server.load_account(keypair)

friendbot.fund_account(pub_key)

tx = TransactionBuilder(
    source_account=acc,
    base_fee=2000,
    network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE
)

for i in range(100):
    tx.append_bump_sequence_op(0)


tx = tx.build()
tx.sign(keypair)

print(server.submit_transaction(tx))