# -*- encoding: utf-8 -*-
from __future__ import division
from __future__ import absolute_import
import subprocess
from time import strftime, localtime

def get_data():
    """
    Returns the status information from several system calls/Python modules as a dictionary
    The following keys are returned in the dictionary:

    - time
    - hostname
    - ip
    - uptime
    - kernel_name
    - top
    - memtotal
    - memfree
    - membuffered
    - memcached
    - swaptotal
    - swapfree
    - temperature
    - top_list
    - cpus (itself a list)
    """
    response_dict = {}
    response_dict["time"] = strftime("%a, %d %b %Y %H:%M:%S", localtime())

    response_dict["hostname"] = subprocess.Popen("hostname", shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')
    response_dict["ip"] = subprocess.Popen("/sbin/ifconfig eth0| grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}'", shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')
    if len(response_dict["ip"]) == 0:
        response_dict["ip"] = subprocess.Popen(" /sbin/ifconfig eth0 | grep 'inet\ ' | cut -d: -f2 | awk '{ print $2 }'", shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')

    response_dict["kernel_name"] = subprocess.Popen("uname -r", shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')
    
    response_dict["memtotal"] = subprocess.Popen("egrep --color 'MemTotal' /proc/meminfo | egrep '[0-9.]{4,}' -o",
                    shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')

    response_dict["memfree"] = subprocess.Popen("egrep --color 'MemFree' /proc/meminfo | egrep '[0-9.]{4,}' -o", shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')
    response_dict["membuffered"] = subprocess.Popen("egrep --color 'Buffers' /proc/meminfo | egrep '[0-9.]{4,}' -o", shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')
    response_dict["memcached"] = subprocess.Popen("egrep --color 'Cached' /proc/meminfo | egrep '[0-9.]{4,}' -o", shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')

    response_dict["swaptotal"] = subprocess.Popen("egrep --color 'SwapTotal' /proc/meminfo | egrep '[0-9.]{4,}' -o", shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')
    response_dict["swapfree"] = subprocess.Popen("egrep --color 'SwapFree' /proc/meminfo | egrep '[0-9.]{4,}' -o", shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')

    response_dict["temperature"] = float(subprocess.Popen("cat /sys/class/thermal/thermal_zone0/temp", shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')) / 1000.0
    response_dict["top"] = subprocess.Popen("top -d 0.5 -b -n2 | grep 'Cpu(s)'|tail -n 1 | awk '{print $2 + $4}'", shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')
    # response_dict["top"] = subprocess.Popen("top -d 0.5 -b -n2 | tail -n 10 | awk '{print $12}'", shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')
    # response_dict["uptime"] = subprocess.Popen("uptime | tail -n 1 | awk '{print $1}'", shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')
    response_dict["uptime"] = subprocess.Popen("uptime | tail -n 1 | awk '{print $3 $4 $5}'", shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')
    response_dict["top_list"] = subprocess.Popen("ps aux --width 30 --sort -rss --no-headers | head  | awk 'BEGIN { OFS = \"-\" } ; {print $3,$4,$11}'", shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')

    response_dict["load_average"] = subprocess.Popen("uptime | awk 'BEGIN { OFS = \"-\" } ; { print $3,$8,$9,$10 }'", shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')
    response_dict["rx"] = subprocess.Popen("ifconfig eth0 | grep \"RX bytes\" | awk '{ print $2 }' | cut -d\":\" -f2", shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')
    response_dict["tx"] = subprocess.Popen("ifconfig eth0 | grep \"TX bytes\" | awk '{ print $6 }' | cut -d\":\" -f2", shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')
    #cpus = subprocess.Popen("mpstat -P ALL | grep -A 5 "+'"%idle"'+ "| tail -n +3 | awk -F"+' " "'+" '{print $ 12 }'",shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8').split('\n')
    cpus = subprocess.Popen("top -d 0.4 -b -n2 | grep \"Cpu\" | tail -n 4 | awk '{print $2 + $4}'", shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8').split('\n')

    try:
        cpus.remove("")
    except ValueError:
        pass
    #subprocess.Popen("top -b -n1 | grep Cpu | sed -r 's@.+:\s([0-9\.]+).+@\1@' | awk '{ print $4 }' | grep \"[0-9]\"|cut -f 1 -d '['", shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8').split('\n')
    cpus_float = [float(c.replace(',','.')) for c in cpus]
    
    response_dict["cpus"] = cpus_float

    return response_dict


