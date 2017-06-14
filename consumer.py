# coding=utf-8

import signal
import time
from Queue import Empty as QueueIsEmpty
from multiprocessing import Process


def ignore_signal():
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    # signal.signal(signal.SIGTERM, signal.SIG_IGN)


class Consumer(Process):
    """A Consumer inherit from multiprocessing.Process, get item from queue, and run until told to stop
         queue: item中介者，这里就是一个进程安全的队列
    poison: 毒药，在发作前一直工作
    consume: 消费方法，由具体的业务指定
        """

    def __init__(self, queue, poison, consume):
        super(Consumer, self).__init__()
        self.queue = queue
        self.poison = poison
        self.consume = consume

    def run(self):
        ignore_signal()
        while not self.poison.is_set():
            try:
                item = self.queue.get(block=True, timeout=1)
                self.consume(item)
            except QueueIsEmpty:
                time.sleep(10)
            except Exception:
                time.sleep(2)
