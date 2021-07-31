from requests.models import Response
from stellar_sdk import Server, Keypair, TransactionBuilder, Network, keypair
import os, sys

from stellar_sdk.signer import Signer
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import friendbot

print("S1Q5")
server = Server("https://horizon-testnet.stellar.org")
keypair = Keypair.from_secret(input("Enter the secret key..."))
pub_key = keypair.public_key

acc = server.load_account(keypair)

issuer = Keypair.random()

tx = TransactionBuilder(
    source_account=acc,
    network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
    base_fee=2000
).append_create_account_op(
    destination=issuer.public_key,
    starting_balance="10"
).append_change_trust_op(
    asset_code="COOL",
    asset_issuer=issuer.public_key
).append_payment_op(
    destination=pub_key,
    amount="1",
    asset_code="COOL",
    asset_issuer=issuer.public_key,
    source=issuer.public_key
).build()

tx.sign(keypair)
tx.sign(issuer)

resp = server.submit_transaction(tx)
print(f"{resp}")