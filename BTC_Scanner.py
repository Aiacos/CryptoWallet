from bit import Key
from tqdm import tqdm
import numpy


pattern = '13zb1hQbWVsc2S7ZTZnP2G4undNNpdh5so'
range_str = '20000000000000000:3ffffffffffffffff'

pattern = '1EhqbyUMvvs7BfL8goY6qcPbD6YKfPqb7e'
range_str = '8:f'




range_min, range_max = (range_str).split(':')

n = int(range_max, 16) - int(range_min, 16)

def generate_account(hex=None):
    privKey= Key.from_int(hex)

    return privKey.to_wif(), privKey.address

def batch(start, end):
    for i in (range(int(range_min, 16), int(range_max, 16) + 1)):
        priv, address = generate_account(i)
        if address == pattern:
            print(priv, address)
            break

if __name__ == "__main__":
    batch()



"""
  n_threads = 10
  futures = []
  
  with concurrent.futures.ThreadPoolExecutor(n_threads) as executor:
      sum = 0 
      for start in range(0, len(l), n_threads):
          futures.append(executor.submit( sum_squares,  l, start, start + n_threads  ) )

      for future in concurrent.futures.as_completed( futures ):
        sum += future.result() 
"""