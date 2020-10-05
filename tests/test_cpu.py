from unittest.mock import patch

from process_utils.system_resources.cpu import Cpu
from process_utils.monitor import Monitor


@patch('psutil.cpu_percent')
@patch('psutil.cpu_count')
def test_cpu_monitor_total(mock_cpu_count, mock_cpu_percent):
    cpu_count = 12
    mock_cpu_percent.return_value = [100] * cpu_count
    mock_cpu_count.return_value = cpu_count

    cpu = Cpu()
    cpu.update()

    monitor = Monitor(cpu)
    monitor.start()

    assert cpu.cpu_percent_total == 100

    monitor.is_running.clear()


@patch('psutil.cpu_percent')
@patch('psutil.cpu_count')
def test_cpu_monitor_logical_cores(mock_cpu_count, mock_cpu_percent):
    cpu_count = 12
    first_logical_cpu = 0
    last_logical_cpu = 11
    mock_cpu_percent.return_value = [100] * cpu_count
    mock_cpu_count.return_value = cpu_count

    cpu = Cpu()
    cpu.update()

    monitor = Monitor(cpu)
    monitor.start()

    assert cpu[first_logical_cpu] == 100
    assert cpu[last_logical_cpu] == 100

    monitor.is_running.clear()
