import os
from typing import List

from mospy import Account, Transaction
from cosmospy_protobuf.cosmos.base.v1beta1.coin_pb2 import Coin
from mospy.clients import HTTPClient
from dotenv import load_dotenv

load_dotenv()


class Faucet:
    def __init__(self, api_node, seed):
        self._client = HTTPClient(api=api_node)
        self._sender_account = Account(
            seed_phrase=seed,
            hrp="stride"
        )
        self._client.load_account_data(account=self._sender_account)

    def construct_sends(self, addresses: List[str]) -> str:
        fee = Coin(
            amount=os.getenv('AMOUNT'),
            denom=os.getenv('DENOM')
        )
        tx = Transaction(
            account=self._sender_account,
            fee=fee,
            gas=int(os.getenv('TX_GAS')),
            chain_id=os.getenv('CHAIN_ID')
        )

        for receipient_address in addresses:
            tx.add_msg(
                tx_type='transfer',
                sender=self._sender_account,
                receipient=receipient_address,
                amount=os.getenv('AMOUNT'),
                denom=os.getenv('DENOM')
            )
        hash, code, log = self._client.broadcast_transaction(transaction=tx)
        return f"{hash} {code} {log}"


if __name__ == '__main__':
    faucet = Faucet(api_node=os.getenv("API_NODE"), seed=os.getenv("SEED"))
    addresses = [
        "stride1yng4v8glvykakc9n57x3na2zkmqhyxfsecnk9v",
        "stride1kgq2nhcc9nlcfvuh0gakcphwqwyg03x45xrdp7",
        "stride1yng4v8glvykakc9n57x3na2zkmqhyxfsecnk9v",
    ]
    print(faucet.construct_sends(addresses))
