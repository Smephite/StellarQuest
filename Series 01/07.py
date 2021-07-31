from requests.models import Response
from stellar_sdk import Server, Keypair, TransactionBuilder, Network, keypair
import os, sys

from stellar_sdk.signer import Signer
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import friendbot

print("S1Q7")
server = Server("https://horizon-testnet.stellar.org")
keypair = Keypair.from_secret(input("Enter the secret key..."))
pub_key = keypair.public_key


channel = Keypair.random()

friendbot.fund_account(channel.public_key)

acc = server.load_account(channel)


tx = TransactionBuilder(
    source_account=acc,
    network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
    base_fee=2000
).append_payment_op(
    channel.public_key,
    amount="1",
    asset_code="XLM",
    source=pub_key
).build()

tx.sign(channel)
tx.sign(keypair)

resp = server.submit_transaction(tx)
print(resp)
