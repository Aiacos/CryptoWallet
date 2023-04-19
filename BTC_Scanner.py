import itertools
from bit import Key
from tqdm import tqdm
import threading

pattern = '13zb1hQbWVsc2S7ZTZnP2G4undNNpdh5so'
range_str = '20000000000000000:3ffffffffffffffff'

pattern = '1DBaumZxUkM4qMQRt2LVWyFJq5kDtSZQot'
range_str = '800:fff'


def generate_account(hex=None):
    privKey = Key.from_int(hex)

    return privKey.to_wif(), privKey.address


def batch(start, end):
    pair_list = []
    for i in tqdm((range(start, end))):
        priv, address = generate_account(i)
        if address == pattern:
            pair_list.append(priv, address)
            break
    print(pair_list)

def batch_single():
    for i in reversed(range(int(range_min, 16), int(range_max, 16) + 1)):
        priv, address = generate_account(i)
        #print('Running: ', priv, address, end="\r", flush=True)
        if address == pattern:
            print(priv, address)
            break


def divide_chunks(l, n):
    return itertools.tee(l, n)
    # looping till length l
    #for i in range(0, len(l), n):
    #    yield l[i:i + n - 1]

def convert_split(range_str, divisions=100):
    range_min, range_max = range_str.split(':')

    int_min = int(range_min, 16)
    int_max = int(range_max, 16)

    l, chunk = generate_batch(int_min, int_max, divisions-1)
    data = {'min': int_min, 'max': int_max, 'range_iterator': l, 'iterator_len': sum(1 for _ in l), 'chunk': chunk}

    return data

def generate_batch(min, max, p=100):
    r = range(min, max)
    chunk = (max - min) / p
    splitted_list = divide_chunks(r, int(chunk))

    return splitted_list, chunk

if __name__ == "__main__":
    k = Key()
    p = k.public_key
    print(p.hex(), len(p.hex()))

    dt = convert_split(range_str, 10)
    print(dt)
    for i in dt['range_iterator']:
        print(i)
        for c in i:
            pass
            #print(c)

    """
    n_threads = 10

    x_range = [*range(int(range_min, 16), int(range_max, 16))]
    #print(x_range)
    x = list(divide_chunks(x_range, n_threads))

    thread_list = []
    for t in range(0, len(x)):
        start, end = x[t][0], x[t][-1]
        cluster = threading.Thread(target=batch, args=(start, end,))
        thread_list.append(cluster)

    for t in thread_list:
        t.start()
    """

