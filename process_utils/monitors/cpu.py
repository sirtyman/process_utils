import psutil

from process_utils.abstract import MonitoredSystemResource
from threading import Lock


class LogicCore:
    def __init__(self, logical_core_percentage):
        self.logical_core_percentage = logical_core_percentage

    def __eq__(self, other):
        return other == self.logical_core_percentage


class Cpu(MonitoredSystemResource):
    def __init__(self):
        self.cpu_percent_total = None
        self.logic_cores_num = psutil.cpu_count()
        self._logical_cores = []

        # ToDo: synchronization
        self._transaction_lock = Lock()

        self._initialize()

    def update(self):
        cpu_percent_by_logic_core = psutil.cpu_percent(1, True)

        self.cpu_percent_total = sum(cpu_percent_by_logic_core) / self.logic_cores_num

        for i, logical_core_percentage in enumerate(cpu_percent_by_logic_core):
            self[i].logical_core_percentage = logical_core_percentage

    def _initialize(self):
        for _ in range(self.logic_cores_num):
            self._logical_cores.append(LogicCore(0))

    def __getitem__(self, index):
        if index < 0 or index > self.logic_cores_num - 1:
            raise KeyError(f'Index must be in range [0, {self.logic_cores_num}]')
        if not isinstance(index, int):
            raise TypeError(f'Index must be integer number')
        return self._logical_cores[index]

    def logic_cores(self):
        for core in self._logical_cores:
            yield core

    def __str__(self):
        usage = f'CPU total usage %: {self.cpu_percent_total}\n'
        usage += 'Per logical core: '

        for core in self.logic_cores():
            usage += f'{core.logical_core_percentage}, '

        return f'{usage}\n'