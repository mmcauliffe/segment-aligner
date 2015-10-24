

import os
import pickle
import numpy
import csv
#import sklearn

from scipy.spatial.distance import euclidean

from acousticsim.multiprocessing import calc_asim
from acousticsim.distance import dtw_distance
from acousticsim.clustering import ClusterNetwork

temp_dir = '/home/michael/Documents/Data/temp/segalign'
temp_textgrid_dir = os.path.join(temp_dir, 'tg')
temp_mfcc_dir = os.path.join(temp_dir, 'mfcc')
temp_align_dir = os.path.join(temp_dir, 'ali')

files = sorted(os.listdir(temp_mfcc_dir))

def path_mapping(files, f):
    for f1 in os.listdir(temp_mfcc_dir):
        if f1 == f:
            continue
        x = os.path.splitext(f)[0]
        y = os.path.splitext(f1)[0]
        yield (x,y)

def call_back(*args):
    return
    print(*args)

def output(asim):
    with open(os.path.join(temp_dir, 'output.txt'), 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['File 1', 'File 2', 'distance'])
        for k,v in sorted(asim.items()):
            writer.writerow([k[0], k[1], v])

if __name__ == '__main__':
    cache = {}
    for f in files:
        name = os.path.splitext(f)[0]
        with open(os.path.join(temp_mfcc_dir, f), 'rb') as fh:
            cache[name] = pickle.load(fh)
            if cache[name].shape != (12,):
                print(name)
                print(cache[name].shape)

    for f in files:
        asim = calc_asim(path_mapping(files, f), cache, euclidean, False, 6, call_back, None)
        break

    #cn = ClusterNetwork(cache)
    #cn.cluster(asim, 'affinity', False)

    #with open(os.path.join(temp_dir, 'cluster.network'), 'wb') as f:
    #    pickle.dump(cn, f)
    output(asim)
    with open(os.path.join(temp_dir, 'asim'), 'wb') as f:
        pickle.dump(asim, f)
