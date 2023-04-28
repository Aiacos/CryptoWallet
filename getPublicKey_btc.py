import sys
import json
import requests
#import bit

def get_btc_public_key_from_txhash(tx_hash):
    url = 'https://api.blockchair.com/bitcoin/dashboards/transaction/' + tx_hash + '?omni=true&privacy-o-meter=true'

    result = requests.get(url)
    transactions_dict = json.loads(str(result.text))

    data_tx = transactions_dict['data'][tx_hash]
    public_key = data_tx['inputs'][-1]['spending_signature_hex'][148:]

    return public_key


if __name__ == "__main__":
    argv = sys.argv
    tx_hash = argv[1]

    public_key = get_btc_public_key_from_txhash(tx_hash)
    print(public_key)