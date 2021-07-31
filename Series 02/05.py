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

claimables = server.claimable_balances().for_claimant(pub_key).call()

claimables = [id['id'] for id in claimables['_embedded']['records']]

tx = TransactionBuilder(
    source_account=acc,
    network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
    base_fee=2000
)

for id in claimables:
    tx.append_claim_claimable_balance_op(
        balance_id=id
    )

tx = tx.build()

tx.sign(keypair)

resp = server.submit_transaction(tx)
print(resp)