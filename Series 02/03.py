from requests.models import Response
from stellar_sdk import Server, Keypair, TransactionBuilder, Network, keypair
import os, sys

from stellar_sdk.signer import Signer
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import friendbot

print("S1Q3")
server = Server("https://horizon-testnet.stellar.org")
keypair = Keypair.from_secret(input("Enter the secret key..."))
pub_key = keypair.public_key

acc = server.load_account(keypair)

payer = Keypair.random()

friendbot.fund_account(payer.public_key)

tx = TransactionBuilder(
    source_account=acc,
    network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
    base_fee=2000
).append_bump_sequence_op(0).build()

tx.sign(keypair)

tx = TransactionBuilder.build_fee_bump_transaction(
    fee_source=payer,
    base_fee=2000,
    inner_transaction_envelope=tx,
    network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE
)

tx.sign(payer)

resp = server.submit_transaction(tx)

print(resp)