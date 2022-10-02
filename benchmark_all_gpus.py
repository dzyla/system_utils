import argparse
import cupy as cp
from joblib import Parallel, delayed
import time

def check_gpu():
    return cp.cuda.runtime.getDeviceCount()

def function(a):
    return cp.sqrt(cp.sum(a**2, axis=-1))

def run_job(gpu):
    global x
    with cp.cuda.Device(gpu):
        while True:
            try:
                a = cp.random.random((1024, 1024, x))
                function(a)
            except cp.cuda.memory.OutOfMemoryError:
                x = x-1
                print(x)
                time.sleep(0.2)

N_GPUS = check_gpu()
print('Found {} GPUs'.format(N_GPUS))
parser = argparse.ArgumentParser(description='Bench GPus')
parser.add_argument('--s', default=600, type=int, help='size of the array')
args = parser.parse_args()
x = args.s
results = Parallel(n_jobs=N_GPUS)(delayed(run_job)(gpu) for gpu in range(0, N_GPUS))
