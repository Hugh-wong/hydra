# coding=utf-8

import signal
import time
from Queue import Empty as QueueIsEmpty
from multiprocessing import Process

def ignore_signal():
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    signal.signal(signal.SIGTERM, signal.SIG_IGN)

class Consumer(Process):
    """A Consumer inherit from process, get task from queue, and run until told to stop"""

    def __init__(self, queue, poison, consume):
        super(Consumer, self).__init__()
        self.queue = queue
        self.poison = poison
        self.consume = consume

    def run(self):
        ignore_signal()
        while not self.poison.is_set():
            try:
                item = self.queue.get(block = True, timeout = 1)
                self.consume(item)
            except QueueIsEmpty:
                time.sleep(10)
            except Exception, e:
                time.sleep(2)