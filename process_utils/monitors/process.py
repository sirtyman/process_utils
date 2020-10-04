import psutil

from process_utils.abstract import MonitoredSystemResource


def find_process_by_name(name):
    for p in psutil.process_iter():
        if p.name() == name:
            process = p
            break
    else:
        RuntimeError('Cannot find any process with name: {}'.format(name))
    return process


class Process(MonitoredSystemResource):
    def __init__(self, process):
        self.process = process
        self.cpu_percent = None
        self.memory_info = None
        self.physical_mem_size = None
        self.virtual_mem_size = None
        self.shared = None
        self.page_faults = None

    def update(self):
        self.cpu_percent = p.cpu_percent(1)
        self.memory_info = p.memory_info()
        self.physical_mem_size = self.memory_info.rss
        self.virtual_mem_size = self.memory_info.vms
        self.shared = self.memory_info.num_page_faults
        self.page_faults = self.memory_info.num_page_faults

    def __str__(self):
        return "CPU: {}, Physical: {}, Virtual: {}, Shared: {}, " \
               "Page Faults: {}".format(self.cpu_percent, self.physical_mem_size,
                                        self.virtual_mem_size,
                                        self.shared,
                                        self.page_faults)


if __name__ == '__main__':
    p = find_process_by_name('pycharm64.exe')
    p_inst = Process(p)
    p_inst.update()
    print(p_inst)
    pass
