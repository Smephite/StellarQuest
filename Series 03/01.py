from requests.models import Response
from stellar_sdk import Server, Keypair, TransactionBuilder, Network, keypair
import os, sys, hashlib

from stellar_sdk.signer import Signer
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import friendbot

server = Server("https://horizon-testnet.stellar.org")
keypair = Keypair.from_secret(input("Enter the secret key..."))
pub_key = keypair.public_key

friendbot.fund_account(pub_key)

acc = server.load_account(keypair)

keyword = input("Keyword? ").encode()
seq = "".join([str(elem) for elem in keyword])

tx = TransactionBuilder(
    source_account=acc,
    network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
    base_fee=2000
).append_bump_sequence_op(int(seq)).build()

tx.sign(keypair)

print(server.submit_transaction(tx))