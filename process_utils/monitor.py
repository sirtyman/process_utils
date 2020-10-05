from threading import Thread, Event
import time


class Monitor(Thread):
    UPDATE_RATE_S = 1

    def __init__(self, *monitored_resource):
        super(Monitor, self).__init__()
        self.monitored_resources = []
        self.monitored_resources = monitored_resource
        self.is_running = Event()

    def run(self):
        self.is_running.set()

        while self.is_running:
            for resource in self.monitored_resources:
                resource.update()
            time.sleep(Monitor.UPDATE_RATE_S)
