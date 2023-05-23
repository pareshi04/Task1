#!/usr/bin/env python
# coding: utf-8

# In[1]:


# to take a screenshot of ssystem
get_ipython().system('pip install psutil')


# In[2]:


#Take snapshot
import psutil
import json
from datetime import datetime
def take_system_snapshot():
    snapshot = {}

    # CPU information
    cpu_info = {}
    cpu_info['cpu_count'] = psutil.cpu_count()
    cpu_info['cpu_percent'] = psutil.cpu_percent(interval=1, percpu=True)
    snapshot['cpu'] = cpu_info

    # Memory information
    mem_info = {}
    mem = psutil.virtual_memory()
    mem_info['total'] = mem.total
    mem_info['available'] = mem.available
    mem_info['used'] = mem.used
    mem_info['percent'] = mem.percent
    snapshot['memory'] = mem_info

    # Disk information
    disk_info = {}
    disks = psutil.disk_partitions()
    for disk in disks:
        disk_usage = psutil.disk_usage(disk.mountpoint)
        disk_info[disk.device] = {
            'total': disk_usage.total,
            'used': disk_usage.used,
            'free': disk_usage.free,
            'percent': disk_usage.percent
        }
    snapshot['disk'] = disk_info

    # Network information
    net_info = {}
    net_io = psutil.net_io_counters()
    net_info['bytes_sent'] = net_io.bytes_sent
    net_info['bytes_received'] = net_io.bytes_recv
    snapshot['network'] = net_info
    # Get the current timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # Get the current timestamp
    current_timestamp = int(datetime.now().timestamp())

    # Formating the current timestamp as a string
    formatted_timestamp = str(current_timestamp)

    snapshot["last_snapshot"] = formatted_timestamp

    snapshot['timestamp'] = timestamp

    return snapshot
    

initial_snapshot = take_system_snapshot()

print(json.dumps(initial_snapshot,indent = 4))


# In[3]:


# comparing
def compare_usage(previous_usage, current_usage, usage_name):
    changes = []
    for i in range(len(previous_usage)):
        change = current_usage[i] - previous_usage[i]
        changes.append(change)
        print(f"{usage_name} {i}: {change}%")
    return changes

def compare_system_snapshot():
    
    current_snapshot = take_system_snapshot()

    # to print the current snapshot
    print("Current Snapshot:")
    print(json.dumps(current_snapshot, indent=4))
    print("\n")
    print("Comparing Both snapshots:")
    # to compare CPU usage
    previous_cpu_percent = initial_snapshot['cpu']['cpu_percent']
    current_cpu_percent = current_snapshot['cpu']['cpu_percent']
    cpu_changes = compare_usage(previous_cpu_percent, current_cpu_percent, 'CPU')

    # to compare memory usage
    previous_mem_percent = initial_snapshot['memory']['percent']
    current_mem_percent = current_snapshot['memory']['percent']
    mem_changes = compare_usage([previous_mem_percent], [current_mem_percent], 'Memory')

    # to compare disk usage
    previous_disk_percent = {}
    current_disk_percent = {}
    for disk in initial_snapshot['disk']:
        previous_disk_percent[disk] = initial_snapshot['disk'][disk]['percent']
        current_disk_percent[disk] = current_snapshot['disk'][disk]['percent']
    disk_changes = compare_usage(list(previous_disk_percent.values()), list(current_disk_percent.values()), 'Disk')

    # to compare network usage
    previous_net_sent = initial_snapshot['network']['bytes_sent']
    previous_net_received = initial_snapshot['network']['bytes_received']
    current_net_sent = current_snapshot['network']['bytes_sent']
    current_net_received = current_snapshot['network']['bytes_received']
    net_sent_change = current_net_sent - previous_net_sent
    net_received_change = current_net_received - previous_net_received
    print(f"Network Sent Data: {net_sent_change} bytes")
    print(f"Network Received Data: {net_received_change} bytes")


compare_system_snapshot()


# In[4]:


# to check for new files
import os
import time
from datetime import datetime

last_snapshot = None

def take_system_snapshot():
    global last_snapshot
    # Capture the system snapshot
    snapshot = {}

    # CPU information
    cpu_info = {}
    cpu_info['cpu_count'] = psutil.cpu_count()
    cpu_info['cpu_percent'] = psutil.cpu_percent(interval=1, percpu=True)
    snapshot['cpu'] = cpu_info

    # Memory information
    mem_info = {}
    mem = psutil.virtual_memory()
    mem_info['total'] = mem.total
    mem_info['available'] = mem.available
    mem_info['used'] = mem.used
    mem_info['percent'] = mem.percent
    snapshot['memory'] = mem_info

    # Disk information
    disk_info = {}
    disks = psutil.disk_partitions()
    for disk in disks:
        disk_usage = psutil.disk_usage(disk.mountpoint)
        disk_info[disk.device] = {
            'total': disk_usage.total,
            'used': disk_usage.used,
            'free': disk_usage.free,
            'percent': disk_usage.percent
        }
    snapshot['disk'] = disk_info

    # Network information
    net_info = {}
    net_io = psutil.net_io_counters()
    net_info['bytes_sent'] = net_io.bytes_sent
    net_info['bytes_received'] = net_io.bytes_recv
    snapshot['network'] = net_info
    # Get the current timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # to get the current timestamp
    current_timestamp = int(datetime.now().timestamp())


    formatted_timestamp = str(current_timestamp)

    snapshot["last_snapshot"] = formatted_timestamp
    snapshot['timestamp'] = timestamp

    return snapshot
    
last_snapshot = int(time.time())
# initial system snapshot
initial_snapshot = take_system_snapshot()

# Print the initial snapshot
print(json.dumps(initial_snapshot,indent = 4))


def find_new_files(system_path):
    global last_snapshot
    current_files = set(os.listdir(system_path))
    new_files = []

    # to compare current files with the files in the last snapshot
    if last_snapshot is not None:
        last_files = set(os.listdir(system_path))
        new_files = list(current_files - last_files)

    # Returning the list of new files
    return new_files

take_system_snapshot()
# need to do some action
time.sleep(30) 
new_files = find_new_files("C:\\Users\\Pareshi Goel\\Documents") # use your system path
print("New files:", new_files)


# In[6]:


# killed process
last_snapshot = []

def take_system_snapshot():
    global last_snapshot
    
    last_snapshot = get_process_list()

def get_process_list():
    
    process_list = []
    for process in psutil.process_iter(['pid', 'name']):
        process_list.append(process.info)
    return process_list

def find_running_processes():
    current_processes = get_process_list()
    running_processes = []

    # to compare current processes with the processes in the last snapshot
    for process in current_processes:
        if process not in last_snapshot:
            running_processes.append(process)

    # Returning the list of running processes
    return running_processes

def find_killed_processes():
    current_processes = get_process_list()
    killed_processes = []

    # Compare processes in the last snapshot with the current processes
    for process in last_snapshot:
        if process not in current_processes:
            killed_processes.append(process)

    return killed_processes

take_system_snapshot()
# we need to perform some actions
time.sleep(10)  # for time delay
running_processes = find_running_processes()
killed_processes = find_killed_processes()

print("Running processes:")
for process in running_processes:
    print(f"PID: {process['pid']}, Name: {process['name']}")

print("Killed processes:")
for process in killed_processes:
    print(f"PID: {process['pid']}, Name: {process['name']}")


# In[ ]:




