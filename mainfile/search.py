import numpy as np
import struct
import decimal
import time
import threading
from sklearn.neighbors import BallTree
from sklearn.externals import joblib

__author__ = 'Zhao Chi'

# vocabulary
voc = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
# flag
flag = 0


def verifydata_deal(test_data_fileName):
    '''
    Preprocessing verify_data
    :param test_data_fileName: verifydata_deal's path
    :return: Preprocessed verify_data
    '''
    global verify_data
    f = open(test_data_fileName, 'rb')
    verify_data_raw = struct.unpack('f' * 102500, f.read(4 * 102500))
    f.close()
    verify_data = np.asarray(verify_data_raw).reshape(-1, 1025)


def run(start, end, name):
    global flag
    # print(name)
    dist_temp, ind_temp = Ball_Tree.query(verify_data[start:end, 1:1025], k=1)
    dist[start:end] = dist_temp
    ind[start:end] = ind_temp
    flag = flag + 1


def search(success_data_dir):
    '''
    search data
    :param success_data_dir: Preprocessed  raw_data
    :return: raw_indexs, raw_distances
    '''

    global idxs, dists
    global dist, ind, flag
    global Ball_Tree
    global loadtimes, searchtimes
    loadtimes = []
    searchtimes = []

    #  定义空数组 Ball tree 查找到的idx+100000
    idxs = np.zeros((verify_data.shape[0], len(voc)))
    dists = np.zeros((verify_data.shape[0], len(voc)))
    # 在此开启多线程模式 读取一个文件占用800M内存
    j = 0
    for i in voc:
        '''load data from BallTree'''
        loadstart = time.time()
        tree_name = success_data_dir + '/data_a' + str(i) + '.pkl'
        Ball_Tree = joblib.load(tree_name)
        loadend = time.time()
        t1 = loadend - loadstart
        loadtimes.append(t1)
        print("加载完毕，用时" + (str(loadend - loadstart)))
        dist = np.zeros((verify_data.shape[0], 1))
        ind = np.zeros((verify_data.shape[0], 1))
        t1 = threading.Thread(target=run, args=(0, 10, 't1'))
        t2 = threading.Thread(target=run, args=(10, 20, 't2'))
        t3 = threading.Thread(target=run, args=(20, 30, 't3'))
        t4 = threading.Thread(target=run, args=(30, 40, 't4'))
        t5 = threading.Thread(target=run, args=(40, 50, 't5'))
        t6 = threading.Thread(target=run, args=(50, 60, 't6'))
        t7 = threading.Thread(target=run, args=(60, 70, 't7'))
        t8 = threading.Thread(target=run, args=(70, 80, 't8'))
        t9 = threading.Thread(target=run, args=(80, 90, 't9'))
        t10 = threading.Thread(target=run, args=(90, 100, 't10'))
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t5.start()
        t6.start()
        t7.start()
        t8.start()
        t9.start()
        t10.start()
        t1.join()
        t2.join()
        t3.join()
        t4.join()
        t5.join()
        t6.join()
        t7.join()
        t8.join()
        t9.join()
        t10.join()
        # 多线程
        while (True):
            if flag == 10:
                idxs[:, j] = idxs[:, j] + (ind + j * 100000).reshape(verify_data.shape[0], )
                dists[:, j] = dists[:, j] + dist.reshape(verify_data.shape[0], )
                j = j + 1
                end = time.time()
                t2 = end - loadend
                searchtimes.append(t2)
                print("从" + tree_name + "中查询完毕，用时" + str(end - loadend))
                flag = 0
                break
    print('多线程执行完毕,正在统计结果')
    return idxs, dists


def outcome_deal(idxs, dists):
    '''
    deal outcomes
    :param idxs: raw_indexs
    :param dists: raw_distances
    :return: time
    '''
    # 输出结果
    min_dists = np.amin(dists, axis=1, keepdims=True)
    min_dists_idx = np.argmin(dists, axis=1)
    min_idxs = idxs[np.arange(verify_data.shape[0]), min_dists_idx].reshape(-1, 1)
    outcomes = np.concatenate((min_idxs, min_dists), axis=1)
    np.savetxt('outcomes.txt', outcomes)  # outcomes包含两列 第一列为id 第二列为欧氏距离
    outcomes_indexs = outcomes[:, 0].astype(np.int32)
    np.savetxt('query__result.txt', outcomes_indexs, fmt='%s')  # query__result 仅包含一列ID
    # 时间计算
    loadtime = np.sum(np.array(loadtimes))
    searchtime = np.sum(np.array(searchtimes))
    print("数据查询完毕,加载耗时" + str(loadtime) + "秒")
    print("数据查询完毕,查询耗时" + str(searchtime) + "秒")
    print("数据查询完毕,共耗时" + str(loadtime + searchtime) + "秒,ID保存在：" + "query__result.txt 中")
    # print(str(min_idxs))
    # 准确度计算
    print("计算准确度中")
    precision = np.sum((min_idxs - verify_data[:, 0]) == 0) / 100
    print("准确度为：" + str(precision))
    return loadtime, searchtime


def main(test_data_fileName, success_data_dir):
    start = time.time()
    verifydata_deal(test_data_fileName)
    idxs, dists = search(success_data_dir)
    loadtime, searchtime = outcome_deal(idxs, dists)
    end = time.time()
    return end - start, loadtime, searchtime
