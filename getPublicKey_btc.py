import sys
import json
import requests
#import bit
from tqdm import tqdm


def test(address):
    url = 'https://api.blockchair.com/bitcoin/dashboards/address/' + address + '?transaction_details=true&omni=true'

    result = requests.get(url)
    transactions_dict = json.loads(str(result.text))

    print(transactions_dict)

def get_btc_transaction_from_address(address):
    url = 'https://blockchain.info/rawaddr/' + address

    result = requests.get(url)
    data = json.loads(str(result.text))
    transactions_out_dict = data['txs']

    return transactions_out_dict

def get_btc_public_key_from_txhash(tx_hash):
    url = 'https://api.blockchair.com/bitcoin/dashboards/transaction/' + tx_hash + '?omni=true&privacy-o-meter=true'

    result = requests.get(url)
    transactions_dict = json.loads(str(result.text))

    data_tx = transactions_dict['data'][tx_hash]
    public_key = data_tx['inputs'][-1]['spending_signature_hex'][148:]

    return public_key


if __name__ == "__main__":
    argv = sys.argv
    #tx_hash = argv[1]

    # for i in tqdm(get_btc_transaction_from_address('12ib7dApVFvg82TXKycWBNpN8kFyiAN1dr'), desc='Searching Public Address'):
    #     try:
    #         public_key = get_btc_public_key_from_txhash(i['hash'])
    #         if public_key:
    #             print('Public Key: ', public_key, ' TX Hash: ', i['hash'])
    #     except:
    #         pass
    test('12ib7dApVFvg82TXKycWBNpN8kFyiAN1dr')