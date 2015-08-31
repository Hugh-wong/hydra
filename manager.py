# coding=utf-8

import sys
import signal
import time
from multiprocessing import Process

from allocator import Allocator, Event

class Manager(object):
    """A manager manage multi allocators, when told to stop, manager would tell the allocator to stop."""

    def __init__(self, cfg_list):
        self.allocator_list = []
        self.event_list = []
        for cfg in cfg_list:
            event = Event()
            cfg.update({'poison': event})
            self.allocator_list.append(Allocator(**cfg))
            self.event_list.append(event)

    def start_all(self):
        """start all the allocators"""
        self.process_list = []
        for allocator in self.allocator_list:
            process = Process(target = allocator.start)
            process.start()
            self.process_list.append(process)

    def stop_all(self, signal, frame):
        """stop all the allocators"""
        for event in self.event_list:
            event.set()
        for process in self.process_list:
            process.join()
        sys.exit()

    @classmethod
    def trigger(cls, cfg_list):
        """outer interface"""
        manager = cls(cfg_list)
        manager.start_all()

        signal.signal(signal.SIGINT, manager.stop_all)
        signal.signal(signal.SIGTERM, manager.stop_all)

        while True: # dead loop might meets many problem, better using a finite loop.
            time.sleep(2)

        manager.stop_all(None, None)
