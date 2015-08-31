# coding=utf-8

import time
import random
from manager import Manager
from multiprocessing import Lock


lock = Lock()

def retrieve_items(need_count):
    with lock:
        print 'need_count = %s' % need_count

    return range(need_count)

def consume_item(item_id):
    t = random.randint(10, 15)
    with lock:
        print '%s is consumed... and need to exec %s seconds' % (item_id, t)
    time.sleep(t)

    with lock:
        print "%s is done, now quit." % (item_id)


if __name__ == "__main__":
    cfg_list = [{'retrieve_items':  retrieve_items,  'consume': consume_item,  'consumer_count':2, 'working_time': [('00:00', '23:59')]}]
    Manager.trigger(cfg_list)
