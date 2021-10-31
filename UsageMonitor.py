from SNMPdata import MonitorInfo
from HostData import Host
from time import sleep
import ReportManager
import datetime
import rrdtool
import os

hosts = [['192.168.1.82', 0], ['127.0.0.1',1], ['192.168.1.74',2]]
monitor = MonitorInfo(hosts = [host[0] for host in hosts])
resource = '1.3.6.1.2.1.7.1.0'
hosts = [Host(monitor, host[0], resource, host[1]) for host in hosts]


if __name__ == '__main__':

	while 1:
		for host in hosts:
			if host.update():
				print(f'El host {host.ip} ha excedido la tarifa')

		sleep(1)