from requests.models import Response
from stellar_sdk import Server, Keypair, TransactionBuilder, Network, keypair
import os, sys

from stellar_sdk.signer import Signer
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import friendbot

print("S1Q4")
server = Server("https://horizon-testnet.stellar.org")
keypair = Keypair.from_secret(input("Enter the secret key..."))
pub_key = keypair.public_key

acc = server.load_account(keypair)

signer_pair = Keypair.random()

print(f"MultiSig is {signer_pair.secret}")

tx_setOp = TransactionBuilder(
    source_account=acc,
    network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
    base_fee=2000
).append_set_options_op(
    signer=Signer.ed25519_public_key(signer_pair.public_key, 1)
).build()

tx_setOp.sign(keypair)

resp = server.submit_transaction(tx_setOp)
print(f"Set Option: {resp}")

tx_multi = TransactionBuilder(
    source_account=acc,
    network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
    base_fee=2000
).append_bump_sequence_op(bump_to=0).build()

tx_multi.sign(signer_pair)

resp = server.submit_transaction(tx_multi)

print(f"Multisiged {resp}")