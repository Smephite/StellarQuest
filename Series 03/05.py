from requests.models import Response
from stellar_sdk import Server, Keypair, TransactionBuilder, Network, keypair
import os, sys
from stellar_sdk.asset import Asset
from stellar_sdk.operation.set_trust_line_flags import TrustLineFlags

from stellar_sdk.signer import Signer
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import friendbot

server = Server("https://horizon-testnet.stellar.org")
keypair = Keypair.from_secret(input("Enter the secret key..."))
pub_key = keypair.public_key


friendbot.fund_account(pub_key)
acc = server.load_account(keypair)

asset = Asset(input("Keycode? "), pub_key)

receiver = Keypair.random()

tx = TransactionBuilder(
    source_account=acc,
    base_fee=2000,
    network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE
).append_create_account_op(
    destination=receiver.public_key,
    starting_balance="10"
).append_set_options_op(
    set_flags=10
).append_change_trust_op(
    asset_code=asset.code,
    asset_issuer=asset.issuer,
    source=receiver.public_key
).append_payment_op(
    destination=receiver.public_key,
    amount="2",
    asset_issuer=asset.issuer,
    asset_code=asset.code
).append_clawback_op(
    asset=asset,
    from_=receiver.public_key,
    amount="1"
).build()

tx.sign(keypair)
tx.sign(receiver)

print(server.submit_transaction(tx))