from abc import abstractmethod


class MonitoredSystemResource:
    @abstractmethod
    def update(self):
        pass
