import os
import sys
from pathlib import Path
import itertools
#from itertools import batched
import more_itertools
from bit import Key
from tqdm import tqdm
import threading
import subprocess
import math

pattern = '13zb1hQbWVsc2S7ZTZnP2G4undNNpdh5so'
range_str = '20000000000000000:3ffffffffffffffff'

#pattern = '1rSnXMr63jdCuegJFuidJqWxUPV7AtUf7'
#range_str = '800000:ffffff'

#pattern = '1DBaumZxUkM4qMQRt2LVWyFJq5kDtSZQot'
#range_str = '800:fff'

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
    #slices = chunks_generator(it, chunk)
    slices = []
    for i in range(int_min, int_max, chunk):
        slices.append(range(i, i + chunk))
    data = {'min': int_min, 'max': int_max, 'iterator_len': sum(1 for _ in slices), 'chunk': chunk, 'iterator': it, 'iterator_slices': slices}

    return data


def sub_iterator(start, end):
    for c in tqdm(range(start, end), desc='Sedondary Loop'):
        priv, address = generate_account(scalar=c)
        #print(priv, address)
        if address == pattern:
            result = priv, address

            return result


def chunks_generator(iterable, size):
    """Generate adjacent chunks of data"""

    it_slice = more_itertools.windowed(iterable, size, size)

    return it_slice


def main_loop(pattern, range_str, sys_call=None, divide=10):
    dt = convert_split(range_str, divide)
    print(dt)
    priority_list = (priority_generator(divide))

    run_by_priority_list = []
    for slice, p in tqdm(zip(dt['iterator_slices'], priority_list), desc='Prepare Loop'):
        int_min = more_itertools.first(slice)
        int_max = more_itertools.last(slice)
        str_hex_range = hex(int_min) + ':' + hex(int_max)

        priority = p[1]
        index = p[0]

        run_by_priority_list.append([priority, index, str_hex_range])

    for i in tqdm(sorted(run_by_priority_list, key=lambda l:l[0], reverse=True), desc='Main Loop'):
        print('\nRunnin Priority: ', i[0], ' Index: ', i[1], ' Range: ', i[2])
        if sys_call:
            sys_call_app(pattern, str_hex_range, sys_call)
        else:
            range_min, range_max = range_str.split(':')
            result = sub_iterator(int(range_min, 16), int(range_max, 16))
            if result:
                print('Result: ', result)
                return


def sys_call_app(pattern, hex_range, function):
    function(pattern, hex_range)

def run_keyhunt_cuda(pattern, hex_range, project='KeyHuntCudaClient', workspace='workspace'):
    path_to_project = Path.home() / 'Documents' / workspace / project / 'x64' / 'Release'
    win_key_cmd = 'KeyHunt-Cuda.exe'
    linux_key_cmd = 'KeyHunt'
    args = '--coin BTC -m address -g --gpui 0 --range ' + str(hex_range).replace('0x', '').lower()

    # Write BTC address to file
    #os.system('echo "' + pattern + '" > btc_list.txt')

    if sys.platform.startswith('win'):
        cmd = ' '.join((str(path_to_project) + '\\' + win_key_cmd, args, pattern))
        print('Running Windows: ', cmd)
        result = subprocess.run(cmd, shell=True, capture_output=True)
        print(result.stdout.decode())
    else:
        cmd = ' '.join((str(path_to_project) + '\\' + linux_key_cmd, args, pattern))
        print('Running Windows: ', cmd)
        result = subprocess.run(cmd, shell=True, capture_output=True)
        print(result.stdout.decode())


def laplaceDistribution2(x, beta=0.5, mu=5):
    """
    Laplace distribution Function
    :param x: float
    :param beta: float
    :param mu: float
    :return: float
    """
    x = x * 10
    core = math.e ** (-1 * abs(x - mu) / beta)
    y = core / (2 * beta)
    return y
def priority_generator(sampling):
    return_list = []
    step = 100 / sampling
    for i in [round(x * (1/sampling), 6) for x in range(0, sampling + 1)]:
        y = laplaceDistribution2(i)
        return_list.append([i, y])

    return return_list


if __name__ == "__main__":
    argv = sys.argv
    #main_loop(argv[1], argv[2], run_keyhunt_cuda)
    main_loop(pattern, range_str, run_keyhunt_cuda)

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
