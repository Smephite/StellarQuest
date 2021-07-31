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


secret = input("Keyword? ")
hash = hashlib.sha256(secret.encode())
tx = TransactionBuilder(
    source_account=acc,
    network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
    base_fee=2000
).append_set_options_op(signer=Signer.sha256_hash(hash.digest(), 254)).build()

tx.sign(keypair)

print(server.submit_transaction(tx))

tx = TransactionBuilder(
    source_account=acc,
    network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
    base_fee=2000
).append_set_options_op(signer=Signer.sha256_hash(hash.digest(), 0)).build()

tx.sign_hashx(secret.encode().hex())

print(hash.hexdigest())
print(secret.encode().hex())
print(server.submit_transaction(tx))