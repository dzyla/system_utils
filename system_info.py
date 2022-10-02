try:
    import platform
    import re
    import socket
    import uuid
    from datetime import datetime
    import os
    import cpuinfo
    import psutil
    import subprocess
except ModuleNotFoundError:
    os.system('pip install py-cpuinfo GPUtil psutil')


def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


def System_information():
    uname = platform.uname()
    fh = open('{}.log'.replace(' ', '').format(uname.node), 'w')
    print("=" * 40, "System Information", "=" * 40, file=fh)

    print(f"System: {uname.system}", file=fh)
    print(f"Node Name: {uname.node}", file=fh)
    print(f"Release: {uname.release}", file=fh)
    print(f"Version: {uname.version}", file=fh)
    print(f"Machine: {uname.machine}", file=fh)
    print(f"Processor: {uname.processor}", file=fh)
    print(f"Processor: {cpuinfo.get_cpu_info()['brand_raw']}", file=fh)
    print(f"Ip-Address: {socket.gethostbyname(socket.gethostname())}", file=fh)
    print(f"Mac-Address: {':'.join(re.findall('..', '%012x' % uuid.getnode()))}", file=fh)

    # Boot Time
    print("=" * 40, "Boot Time", "=" * 40, file=fh)
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)
    print(f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}", file=fh)

    # print CPU information
    print("=" * 40, "CPU Info", "=" * 40, file=fh)
    # number of cores
    print("Physical cores:", psutil.cpu_count(logical=False), file=fh)
    print("Total cores:", psutil.cpu_count(logical=True), file=fh)
    # CPU frequencies
    cpufreq = psutil.cpu_freq()
    print(f"Max Frequency: {cpufreq.max:.2f}Mhz", file=fh)
    print(f"Min Frequency: {cpufreq.min:.2f}Mhz", file=fh)
    print(f"Current Frequency: {cpufreq.current:.2f}Mhz", file=fh)
    # CPU usage
    # print("CPU Usage Per Core:")
    # for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
    #     print(f"Core {i}: {percentage}%")
    # print(f"Total CPU Usage: {psutil.cpu_percent()}%")

    # Memory Information
    print("=" * 40, "Memory Information", "=" * 40, file=fh)
    # get the memory details
    svmem = psutil.virtual_memory()
    print(f"Total: {get_size(svmem.total)}", file=fh)
    print(f"Available: {get_size(svmem.available)}", file=fh)
    print(f"Used: {get_size(svmem.used)}", file=fh)
    print(f"Percentage: {svmem.percent}%", file=fh)

    print("=" * 20, "SWAP", "=" * 20, file=fh)
    # get the swap memory details (if exists)
    swap = psutil.swap_memory()
    print(f"Total: {get_size(swap.total)}", file=fh)
    print(f"Free: {get_size(swap.free)}", file=fh)
    print(f"Used: {get_size(swap.used)}", file=fh)
    print(f"Percentage: {swap.percent}%", file=fh)

    # Disk Information
    print("=" * 40, "Disk Information", "=" * 40, file=fh)
    print("Partitions and Usage:", file=fh)
    # get all disk partitions
    partitions = psutil.disk_partitions()
    for partition in partitions:
        if 'loop' not in str(partition.device):
            print(f"=== Device: {partition.device} ===", file=fh)
            print(f"  Mountpoint: {partition.mountpoint}", file=fh)
            print(f"  File system type: {partition.fstype}", file=fh)
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
            except:
                # this can be catched due to the disk that
                # isn't ready
                continue
            print(f"  Total Size: {get_size(partition_usage.total)}", file=fh)
            print(f"  Used: {get_size(partition_usage.used)}", file=fh)
            print(f"  Free: {get_size(partition_usage.free)}", file=fh)
            print(f"  Percentage: {partition_usage.percent}%", file=fh)
    # get IO statistics since boot
    disk_io = psutil.disk_io_counters()
    print(f"Total read: {get_size(disk_io.read_bytes)}", file=fh)
    print(f"Total write: {get_size(disk_io.write_bytes)}", file=fh)

    ## Network information
    print("=" * 40, "Network Information", "=" * 40, file=fh)
    ## get all network interfaces (virtual and physical)
    if_addrs = psutil.net_if_addrs()
    for interface_name, interface_addresses in if_addrs.items():
        for address in interface_addresses:
            print(f"=== Interface: {interface_name} ===", file=fh)
            if str(address.family) == 'AddressFamily.AF_INET':
                print(f"  IP Address: {address.address}", file=fh)
                print(f"  Netmask: {address.netmask}", file=fh)
                print(f"  Broadcast IP: {address.broadcast}", file=fh)
            elif str(address.family) == 'AddressFamily.AF_PACKET':
                print(f"  MAC Address: {address.address}", file=fh)
                print(f"  Netmask: {address.netmask}", file=fh)
                print(f"  Broadcast MAC: {address.broadcast}", file=fh)
    ##get IO statistics since boot
    net_io = psutil.net_io_counters()
    print(f"Total Bytes Sent: {get_size(net_io.bytes_sent)}", file=fh)
    print(f"Total Bytes Received: {get_size(net_io.bytes_recv)}", file=fh)

    print("=" * 40, "GPU Info", "=" * 40, file=fh)
    import GPUtil
    Gpus = GPUtil.getGPUs()
    gpulist = []
    for gpu in Gpus:
        print(f"=== {gpu.name} ===", file=fh)
        print('\tgpu.id:', gpu.id, file=fh)

        print('\ttotal GPU:', gpu.memoryTotal, file=fh)
        print(f"\tMemory free {gpu.memoryFree}MB", file=fh)
        print('\tGPU usage:', gpu.memoryUsed, file=fh)
        print('\tgpu use proportion:', gpu.memoryUtil * 100, file=fh)
        print('\tGPU Temperature:', str(gpu.temperature) + " C", file=fh)

    print('Driver version: ', gpu.driver, file=fh)
    os.system('nvcc -V > .tmp')
    cuda_ver = open('.tmp').read()
    print(cuda_ver, file=fh)
    os.remove('.tmp')
    fh.close()


if __name__ == "__main__":
    System_information()
