# print("程序开始执行,请稍后")
import time
from mainfile import search
from mainfile import data_deal


def run_process(base_data_fileName, test_data_fileName, success_data_dir):
    start = time.time()
    deal_time = data_deal.main(base_data_fileName, success_data_dir)
    chazhao_time, load_time, search_time = search.main(test_data_fileName, success_data_dir)
    end = time.time()
    zong_time = end - start
    return {
        "processing": deal_time,
        "look_up": chazhao_time,
        "load": load_time,
        "search": search_time,
        "times": zong_time
    }
