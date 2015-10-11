# coding=utf-8

import math
import random
from manager import Manager


def retrieve_items(need_count):
    return [random.randint(300000, 600000) for _ in xrange(need_count)]


def is_prime(n):
    if not isinstance(n, int):
        raise TypeError("argument passed to is_prime is not of 'int' type")
    if n < 2:
        return False
    if n == 2:
        return True
    max = int(math.ceil(math.sqrt(n)))
    i = 2
    while i <= max:
        if n % i == 0:
            return False
        i += 1
    return True

def consume_item(n):
    return sum([x for x in xrange(2,n) if is_prime(x)])


if __name__ == "__main__":
    cfg_list = [{'retrieve_items':  retrieve_items,
                 'consume': consume_item,
                 'consume_timeout': 20,
                 'consumer_count':4,
                 'working_time': [('00:00', '23:59')]
                 }]
    Manager.trigger(cfg_list)