import psutil

from process_utils.system_resources.abstract import MonitoredSystemResource


def find_by_name(name):
    for p in psutil.process_iter():
        if p.name() == name:
            process = p
            break
    else:
        RuntimeError('Cannot find any process with name: {}'.format(name))
    return process


class ProcessData:
    def __init__(self, cpu_usage, size_in_physical_mem, size_in_virtual_mem,
                 size_in_shared_mem, num_page_faults):
        self.cpu_usage = cpu_usage
        self.size_in_physical_mem = size_in_physical_mem
        self.size_in_virtual_mem = size_in_virtual_mem
        self.size_in_shared_mem = size_in_shared_mem
        self.num_page_faults = num_page_faults


class ProcessUpdater(MonitoredSystemResource):
    def __init__(self, process, collector, interval=1):
        self.process = process
        self.collector = collector
        self.interval = interval

    def update(self):
        cpu_percent = self.process.cpu_percent(self.interval)
        memory_info = self.process.memory_info()
        size_in_physical_mem = memory_info.rss
        size_in_virtual_mem = memory_info.vms
        size_in_shared_mem = memory_info.shared
        num_page_faults = memory_info.num_page_faults

        process_data = ProcessData(cpu_percent, size_in_physical_mem, size_in_virtual_mem,
                                   size_in_shared_mem, num_page_faults)
        self.collector.collect(process_data)


class ProcessDataCollector:
    def __init__(self):
        self.process_metrics = []

    def collect(self, process_metric):
        self.process_metrics.append(process_metric)