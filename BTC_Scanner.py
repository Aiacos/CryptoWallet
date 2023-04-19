import sys
import itertools
#from itertools import batched
import more_itertools
from bit import Key
from tqdm import tqdm
import threading

pattern = '13zb1hQbWVsc2S7ZTZnP2G4undNNpdh5so'
range_str = '20000000000000000:3ffffffffffffffff'

pattern = '1LeBZP5QCwwgXRtmVUvTVrraqPUokyLHqe'
range_str = '200:3ff'


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
    chunk = int((int_max - int_min) / (divisions))

    it = range(int_min, int_max)
    l = chunks_generator(it, chunk)
    data = {'min': int_min, 'max': int_max, 'iterator_len': sum(1 for _ in l), 'chunk': chunk, 'range_iterator': l}

    return data


def sub_iterator(it):
    int_min = more_itertools.first(it)
    int_max = more_itertools.last(it)

    print(int_min, int_max)
    print(it)
    for c in tqdm(it, desc='Sedondary Loop'):
        print(c)
        priv, address = generate_account(scalar=c)
        #print(priv, address)
        if address == pattern:
            result = priv, address
            print('Result: ', result)

            return result


def chunks_generator(iterable, size):
    """Generate adjacent chunks of data"""

    it_slice = more_itertools.divide(size, iterable)

    return it_slice


def main_loop(pattern, range_str):
    dt = convert_split(range_str, 100)
    print(dt)
    for i in tqdm(dt['range_iterator'], desc='Main Loop'):
        print('Result: ', sub_iterator(i))


if __name__ == "__main__":
    argv = sys.argv
    main_loop(argv[1], argv[2])
    #main_loop(pattern, range_str)

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
