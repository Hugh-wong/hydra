# coding=utf-8

import datetime
import time
from Queue import Full as QueueIsFull
from multiprocessing import Process, Queue, Event
from consumer import Consumer, ignore_signal

class Allocator(object):
    """A Allocator manage multi consumers, feed them with items"""

    def __init__(self, retrieve_items, consume, consumer_count, working_time, poison):
        self.retrieve_items = retrieve_items
        self.consume = consume
        self.consumer_count = consumer_count
        self.queue = Queue(consumer_count)
        self.working_time = self.parse_working_time(working_time)
        self.poison = poison

    def parse_working_time(self, working_time):
        result_list = []
        if not working_time:
            result_list = ((datetime.time(0, 0), datetime.time(23, 59)),)
        else:
            try:
                for i in working_time:
                    result_list.append((datetime.time(*map(int, i[0].split(':'))),
                                        datetime.time(*map(int, i[1].split(':')))
                                        ))
            except Exception:
                print "wrong working_time, raw is %s, using default working_time" % working_time
                result_list = ((datetime.time(0, 0), datetime.time(23, 59)),)
        return result_list

    def is_time_todo(self):
        nowtime = datetime.datetime.now().time()
        for i in self.working_time:
            if i[1] >= nowtime and i[0] <= nowtime:
                return True
        return False

    def wake_consumer(self):
        self.consumer_poison_list = []
        self.consumer_list = []
        for _ in xrange(self.consumer_count):
            tmp_poison = Event()
            consumer = Consumer(queue = self.queue, poison = tmp_poison, consume = self.consume)
            consumer.start()
            self.consumer_poison_list.append(tmp_poison)
            self.consumer_list.append(consumer)

    def add_items(self, item_list):
        while item_list:
            try:
                item = item_list.pop()
                self.queue.put(item, block = True, timeout = 1)
            except IndexError:
                break
            except QueueIsFull:
                item_list.append(item)
                time.sleep(20)

    def start(self):
        ignore_signal()
        self.wake_consumer()
        while not self.poison.is_set():
            if self.is_time_todo():
                item_list = self.get_items(need_count = self.consumer_count - self.queue.qsize())
                self.add_items(item_list)
            time.sleep(10)

        self.stop()

    def get_items(self, need_count):
        if need_count > 0:
            try:
                return self.retrieve_items(need_count)
            except Exception:
                return []
        else:
            return []

    def stop(self):
        for poison in self.consumer_poison_list:
            poison.set()
        for consumer in self.consumer_list:
            consumer.join()
