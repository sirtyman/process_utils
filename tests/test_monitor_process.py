import time

from unittest.mock import Mock

from process_utils.system_resources.process import ProcessUpdater, \
    ProcessDataCollector, ProcessData
from process_utils.monitor import Monitor


class MemoryInfoFake:
    def __init__(self):
        self.rss = 10
        self.vms = 10
        self.shared = 10
        self.num_page_faults = 10


def test_monitor_process():
    mock_psutil_process = Mock()
    mock_psutil_process.cpu_percent = Mock(side_effect=[10, 20, 30, 10, 20, 30])

    mock_psutil_process.memory_info = Mock(side_effect=[MemoryInfoFake()] * 2)

    collector = ProcessDataCollector()
    process_data_updater = ProcessUpdater(mock_psutil_process, collector)
    process_data_updater.update()

    assert len(collector.process_metrics) == 1
    assert collector.process_metrics[-1].cpu_usage == 10
    assert collector.process_metrics[-1].size_in_physical_mem == 10
    assert collector.process_metrics[-1].size_in_virtual_mem == 10
    assert collector.process_metrics[-1].size_in_shared_mem == 10
    assert collector.process_metrics[-1].num_page_faults == 10

    process_data_updater.update()
    assert len(collector.process_metrics) == 2


