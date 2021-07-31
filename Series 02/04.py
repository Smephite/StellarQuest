from requests.models import Response
from stellar_sdk import Server, Keypair, TransactionBuilder, Network, keypair
import os, sys, time
from stellar_sdk.asset import Asset
from stellar_sdk.operation.create_claimable_balance import ClaimPredicate, ClaimPredicateType, Claimant

from stellar_sdk.signer import Signer
from stellar_sdk.xdr import claim_predicate
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import friendbot

print("S1Q4")
server = Server("https://horizon-testnet.stellar.org")
keypair = Keypair.from_secret(input("Enter the secret key..."))
pub_key = keypair.public_key

acc = server.load_account(keypair)

tx = TransactionBuilder(
    source_account=acc,
    network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
    base_fee=2000
).append_create_claimable_balance_op(
    asset=Asset.native(),
    amount="100",
    claimants=
    [
        Claimant
        (
            destination=pub_key,
            predicate=ClaimPredicate.predicate_not
            (
                ClaimPredicate.predicate_before_absolute_time(int(time.time()))
            )
        )
    ]
).build()

tx.sign(keypair)

resp = server.submit_transaction(tx)
print(resp)