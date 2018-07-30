# 导入包
import os
import time
import struct
import numpy as np
from sklearn.externals import joblib
from sklearn.neighbors import BallTree

__author__ = 'Zhao Chi'

global nx
global ny
ny = 100000
nx = 1025


def data_split(base_data_fileName, success_data_dir):
    '''
    file split : split -b 410000000 -a 2 base_vector.fea data_
    each file after split have 100000 rows
    save "npy" files
    '''
    global voc
    sh = os.system(
        "split -b 410000000 -a 2 {baseFileName} {successDataDir}/data_".format(baseFileName=base_data_fileName,
                                                                               successDataDir=success_data_dir))
    voc = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']  # build vocabulary


def data_unpack(nx, ny, data_name):
    '''
    binary files' read
    :param nx: row number
    :param ny: column number
    :param data_name: name of binary file
    :return: a numpy array
    '''
    f = open(data_name, "rb")
    item = np.zeros((ny, nx))
    for j in range(ny):
        data = f.read(4 * 1025)
        elem = struct.unpack("f" * 1025, data)
        item[j, :] = elem
    f.close()
    return item


def data_deal(success_data_dir):
    '''
    data split
    :param success_data_dir: data_path
    :return:
    '''
    for i in voc:
        data_name = success_data_dir + '/data_a' + str(i)
        data = data_unpack(nx, ny, data_name)
        Ball_Tree = BallTree(data[:, 1:1025], leaf_size=100000)
        joblib.dump(Ball_Tree, data_name + '.pkl')
        sh = os.system("rm -f " + data_name)


def main(base_data_fileName, success_data_dir):
    start = time.time()
    data_split(base_data_fileName, success_data_dir)
    data_deal(success_data_dir)
    end = time.time()
    return end - start
