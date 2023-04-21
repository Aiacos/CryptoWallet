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


def main_loop(pattern, range_str, sys_call=None, divide=1000000):
    dt = convert_split(range_str, divide)
    print(dt)
    for slice in tqdm(dt['iterator_slices'], desc='Main Loop'):
        int_min = more_itertools.first(slice)
        int_max = more_itertools.last(slice)
        str_hex_range = hex(int_min) + ':' + hex(int_max)

        if sys_call:
            sys_call_app(pattern, str_hex_range, sys_call)
        else:
            result = sub_iterator(int_min, int_max)
            if result:
                print('Result: ', result)
                return


def sys_call_app(pattern, hex_range, function):
    function(pattern, hex_range)

def run_keyhunt_cuda(pattern, hex_range, project='KeyHuntCudaClient', workspace='workspace'):
    path_to_project = Path.home() / 'Documents' / workspace / project / 'x64' / 'Release' / '\\'
    win_key_cmd = './KeyHunt-Cuda.exe'
    linux_key_cmd = './KeyHunt'
    args = '-c BTC -m address -g --gpui 0 -r ' + hex_range

    # Write BTC address to file
    #os.system('echo "' + pattern + '" > btc_list.txt')

    if sys.platform.startswith('win'):
        cmd = ' '.join((path_to_project + win_key_cmd, args, pattern))
        subprocess.run(cmd, shell=True, capture_output=True)
        print('Running Windows: ', cmd.replace('\\', '/'))
    else:
        os.system('cd ' + str(path_to_project))
        cmd = ' '.join((linux_key_cmd, args, pattern))
        subprocess.run(cmd)
        print('Running UNIX: ', cmd)


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
