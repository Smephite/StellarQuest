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

acc = server.load_account(keypair)
new_acc = Keypair.random()

tx = TransactionBuilder(
    base_fee=2000,
    network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
    source_account=acc
).append_begin_sponsoring_future_reserves_op(
    sponsored_id=new_acc.public_key
).append_create_account_op(
    destination=new_acc.public_key,
    starting_balance="0"
).append_end_sponsoring_future_reserves_op(
    source=new_acc.public_key
).build()

tx.sign(new_acc)
tx.sign(keypair)

resp = server.submit_transaction(tx)
print(resp)


tx = TransactionBuilder(
    source_account=acc,
    network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
    base_fee=2000
).append_payment_op(
    destination=new_acc.public_key,
    amount="10",
    asset_code="XLM"
).append_revoke_account_sponsorship_op(
    account_id=new_acc.public_key
).build()

tx.sign(keypair)

resp = server.submit_transaction(tx)

print(resp)