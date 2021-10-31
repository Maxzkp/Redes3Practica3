import ReportManager
import UsageMonitor

x = 1
for host in UsageMonitor.hosts:
	print(f'{x}) {host.ip}')
	x += 1

op = int(input('\n\nElija un host para generar reporte: '))

ReportManager.makeReport(UsageMonitor.hosts[op-1])
