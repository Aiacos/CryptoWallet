import itertools
from bit import Key
from tqdm import tqdm
import threading

pattern = '13zb1hQbWVsc2S7ZTZnP2G4undNNpdh5so'
range_str = '20000000000000000:3ffffffffffffffff'

pattern = '1DBaumZxUkM4qMQRt2LVWyFJq5kDtSZQot'
range_str = '800:fff'


def generate_account(hex=None, scalar=None):
    if scalar:
        privKey = Key.from_int(scalar)
        return privKey.to_wif(), privKey.address
    if hex:
        privKey = Key.from_int(scalar)
        return privKey.to_wif(), privKey.address

    privKey = Key()
    return privKey.to_wif(), privKey.address


def convert_split(range_str, divisions=100):
    range_min, range_max = range_str.split(':')

    int_min = int(range_min, 16)
    int_max = int(range_max, 16)
    chunk = (int_max - int_min) / (divisions - 1)

    it = range(int_min, int_max)
    l = itertools.tee(it, divisions)
    data = {'min': int_min, 'max': int_max, 'iterator_len': sum(1 for _ in l), 'chunk': chunk, 'range_iterator': l}

    return data

################### OLD ###################
def divide_chunks(l, n):
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n - 1]

def generate_batch(min, max, p=100):
    r = range(min, max)
    chunk = (max - min) / p
    splitted_list = divide_chunks(r, int(chunk))

    return splitted_list, chunk

if __name__ == "__main__":
    dt = convert_split(range_str, 100)
    print(dt)
    for i in tqdm(dt['range_iterator']):
        #print(i)
        for c in i:
            priv, address = generate_account(scalar=c)
            #print(priv, address)
            if address == pattern:
                print('Result: ', priv, address)
                break
        else:
            continue
        break


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

