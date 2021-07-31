from requests.models import Response
from stellar_sdk import Server, Keypair, TransactionBuilder, Network, keypair, Asset
import os, sys, json

from stellar_sdk.signer import Signer
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import friendbot

print("S1Q8")
server = Server("https://horizon-testnet.stellar.org")
keypair = Keypair.from_secret(input("Enter the secret key..."))
pub_key = keypair.public_key

acc = server.load_account(keypair)

srt = Asset("SRT", "GCDNJUBQSX7AJWLJACMJ7I4BC3Z47BQUTMHEICZLE6MU4KQBRYG5JY6B")
native = Asset("XLM")


path_server = Server.strict_receive_paths(server, source=[native], destination_amount="50", destination_asset=srt).call()
path = [Asset(asset['destination_asset_code'], asset['destination_asset_issuer']) for asset in path_server['_embedded']['records']]

tx = TransactionBuilder(
    source_account=acc,
    network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
    base_fee=2000
).append_change_trust_op(
    asset_code=srt.code, asset_issuer=srt.issuer
).append_path_payment_strict_send_op(
    destination=pub_key,
    send_code="XLM",
    send_issuer=None,
    send_amount="10",
    dest_code="SRT",
    dest_min="1",
    dest_issuer=srt.issuer,
    path=path
).build()

tx.sign(keypair)

resp = server.submit_transaction(tx)

print(resp)