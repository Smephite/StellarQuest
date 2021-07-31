from requests.models import Response
from stellar_sdk import Server, Keypair, TransactionBuilder, Network, keypair
import os, sys, hashlib
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import friendbot

print("S1Q1")
server = Server("https://horizon-testnet.stellar.org")
private_key = Keypair.from_secret(input("Enter the secret key..."))
pub_key = private_key.public_key

funder = Keypair.random()
funder_pub = funder.public_key

print("Funding account")
friendbot.fund_account(funder_pub)

base_fee = 20000
funder_acc = server.load_account(funder_pub)
hash = hashlib.sha256()
hash.update(input("Input hash secret: ").encode())
tx = TransactionBuilder(source_account=funder_acc,
                        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
                        base_fee=base_fee
                        ).append_create_account_op(
                            destination=pub_key,
                             starting_balance="5000"
                        ).add_hash_memo(hash.hexdigest()).build()

tx.sign(funder)

response = server.submit_transaction(tx)

print(f"Server response {response}")


