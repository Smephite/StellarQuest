from requests.models import Response
from stellar_sdk import Server, Keypair, TransactionBuilder, Network, keypair
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import friendbot

print("S1Q2")
server = Server("https://horizon-testnet.stellar.org")
keypair = Keypair.from_secret(input("Enter the secret key..."))
pub_key = keypair.public_key

acc = server.load_account(keypair)

other = Keypair.random().public_key

tx = TransactionBuilder(
    source_account=acc,
    network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
    base_fee=20000
).append_create_account_op(
    destination=other,
    starting_balance="1"
).append_payment_op(
    destination=other,
    amount="10",
    asset_code="XLM"
).build()

tx.sign(keypair)

resp = server.submit_transaction(tx)

print(resp)