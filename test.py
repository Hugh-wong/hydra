# coding=utf-8

from manager import Manager
from multiprocessing import Lock


lock = Lock()

def retrieve_items(need_count):
    with lock:
        print 'need_count = %s' % need_count

    return range(need_count)

def consume_item(item_id):
    with lock:
        print '%s is consumed...' % item_id

if __name__ == "__main__":
    cfg_list = [{'retrieve_items':  retrieve_items, 'consume': consume_item, 'consumer_count':2, 'working_time': [('00:00', '23:59')]}]
    Manager.trigger(cfg_list)
