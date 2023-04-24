import sys
import web3
from eth_account._utils.signing import extract_chain_id, to_standard_v
from eth_account._utils.legacy_transactions import ALLOWED_TRANSACTION_KEYS
from eth_account._utils.legacy_transactions import serializable_unsigned_transaction_from_dict
from eth_keys.datatypes import Signature
import requests
import json
from tqdm import tqdm


infura_endpoint = 'https://mainnet.infura.io/v3/972b4b8a084b434bba97948637e946be'
infura_API = 'PY49HDD1DPEEX9PE6PUZ56VP38493ARBGM'

w3 = web3.Web3(web3.HTTPProvider(infura_endpoint))


def get_tx_list(address, tx_count):
    url = 'https://api.etherscan.io/api?module=account&action=txlist&address=' + address + '&startblock=0&endblock=99999999&page=1&offset=' + tx_count + '&sort=asc&apikey=' + infura_API
    # https://api.etherscan.io/api?module=account&action=txlist&address=0x324e2D42D7B65E5574787C331DfaA29d2Dead666&startblock=0&endblock=99999999&page=1&offset=10&sort=asc&apikey=PY49HDD1DPEEX9PE6PUZ56VP38493ARBGM

    result = requests.get(url)
    transactions_dict = json.loads(str(result.text))

    return transactions_dict


def pub_key_from_tx_eth1(txid):
    try:
        tx = w3.eth.getTransaction(txid)

        s = w3.eth.account._keys.Signature(vrs=(
            to_standard_v(extract_chain_id(tx.v)[1]),
            w3.toInt(tx.r),
            w3.toInt(tx.s)
        ))
    except:
        tx = w3.eth.get_transaction(txid)
        # print('tx.hash: ', tx.hash)

        s = w3.eth.account._keys.Signature(vrs=(
            to_standard_v(extract_chain_id(tx.v)[1]),
            w3.to_int(tx.r),
            w3.to_int(tx.s)
        ))

    #print("signature: ", s)

    tt = {k: tx[k] for k in ALLOWED_TRANSACTION_KEYS - {'chainId', 'data'}}
    tt['data'] = tx.input
    tt['chainId'] = extract_chain_id(tx.v)[0]

    #print("Transaction: ", tt)

    ut = serializable_unsigned_transaction_from_dict(tt)

    # print("Hash:: ", ut.hash())
    #print("Public kye: ", s.recover_public_key_from_msg_hash(ut.hash()))

    check_address = s.recover_public_key_from_msg_hash(ut.hash()).to_checksum_address()
    #print('Check Address: ', check_address)
    if check_address == tx['from']:
        #print('Found: ', s.recover_public_key_from_msg_hash(ut.hash()), ' From: ', check_address)
        #return s.recover_public_key_from_msg_hash(ut.hash())
        return ({'public_key': s.recover_public_key_from_msg_hash(ut.hash()), 'address': tx['from']})
    else:
        #print('Not Found')
        return None

def pub_key_from_tx_eth2(txid, chain='ETH'):
    """Obtain the public key from an Ethereum transaction
    """
    w3test = web3.Web3(web3.HTTPProvider(infura_endpoint))
    transaction = w3test.eth.get_transaction(txid)
    vrs = (to_standard_v(transaction['v']),
           int.from_bytes(transaction['r'], "big"),
           int.from_bytes(transaction['s'], "big"))
    signature = Signature(vrs=vrs)
    tx_dict = {'nonce': transaction.nonce,
               'gasPrice': transaction.gasPrice,
               'gas': transaction.gas,
               'to': transaction.to,
               'value': transaction.value
    }
    if chain == "ETH":
        tx_dict['chainId'] = "0x01"
    elif chain == "tETH":
        tx_dict['chainId'] = "0x03"
    if 'input' in transaction:
        tx_dict['data'] = transaction['input']
    serialized_tx = serializable_unsigned_transaction_from_dict(tx_dict)
    rec_pub = signature.recover_public_key_from_msg_hash(serialized_tx.hash())
    if rec_pub.to_checksum_address() != transaction['from']:
        #print('Wrong:', rec_pub.to_checksum_address(), ' From: ', transaction['from'])
        return None
        #raise ValueError("Unable to obtain public key from transaction: " + f"{txid}")
    return({'public_key': rec_pub, 'address': transaction['from']})


if __name__ == "__main__":
    argv = sys.argv
    address = argv[1]
    tx_count = argv[2]

    publicKey_list = []
    for i in tqdm(get_tx_list(address, tx_count)["result"], desc='Searching Public Address'):
        #print(i['hash'])
        p_key1 = pub_key_from_tx_eth1(i['hash'])
        #p_key2 = pub_key_from_tx_eth2(i['hash'])
        if p_key1:
            publicKey_list.append(p_key1)
            #publicKey_list.append(p_key2)


    for i in [dict(t) for t in {tuple(d.items()) for d in publicKey_list}]:
        if i['address'] == address:
            print(i)
    else:
        pass
        #print('Not Correct: ', i)