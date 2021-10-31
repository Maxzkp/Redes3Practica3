import datetime
import os

ULVLNAMES = ['Low', 'Mid', 'High']
ULVLCOST = [0.5, 0.5, 0.5]
pageavg = 1000
ULVLS = [30*pageavg, 300*pageavg, 2000*pageavg]

class Host():
	def __init__(self, monitor, ip, resource, ulvl = 0):
		self.ip = ip
		self.monitor = monitor
		self.resource = resource
		self.exceded = False
		if os.path.exists(f'hostdata/{ip}.usg'):
			with open(f'hostdata/{ip}.usg', 'r') as f:
				lines = f.readlines()
				self.ulvl = int(lines[0])
				self.reads = list([line.strip().split('/') for line in lines[1:]])
				self.reads = list([[int(reg[0]),reg[1]] for reg in self.reads])
				if len(self.reads) >= 3:
					self.exceded = True
		else:
			self.ulvl = ulvl
			self.reads = [[self.monitor.snmpConsult(self.ip, self.resource), str(datetime.datetime.now())]]
			self.reads.append(self.reads[0])
			self.writefile()

	def writefile(self):
		with open(f'hostdata/{self.ip}.usg', 'w') as f:
			f.write(f'{self.ulvl}')
			for reg in self.reads:
				info = f'{reg[0]}/{reg[1]}'
				f.write(f'\n{info}')	

	def update(self):
		newinfo = self.monitor.snmpConsult(self.ip, self.resource)
		self.reads[1] = [newinfo, datetime.datetime.now()]

		if not self.exceded and newinfo - self.reads[0][0] > ULVLS[self.ulvl]:
			self.reads.append([newinfo, datetime.datetime.now()])
			self.exceded = True
		self.writefile()
		return self.exceded

	def ulvlname(self):
		return ULVLNAMES[self.ulvl]

	def costtable(self):
		costs = []
		if self.exceded:
			costs.append(['Normal usage', 
						  int(ULVLS[self.ulvl]), 
						  str(self.reads[0][1]), 
						  str(self.reads[2][1]), 
						  float((ULVLS[self.ulvl])*ULVLCOST[self.ulvl])])
			costs.append(['Exceded usage', 
						  int(self.reads[1][0] - ULVLS[self.ulvl]), 
						  str(self.reads[2][1]), 
						  str(self.reads[1][1]), 
						  float((self.reads[1][0] - ULVLS[self.ulvl])*ULVLCOST[self.ulvl]*2)])
		else:
			costs.append(['Normal usage', 
						  self.reads[1][0] - self.reads[0][0], 
						  self.reads[0][1], 
						  self.reads[1][1], 
						  float(self.reads[1][0] - self.reads[0][0])*ULVLCOST[self.ulvl]])
		return costs

	def __str__(self):
		info = f'{self.ip} | {self.ulvl}'
		for reg in self.reads:
			info += f'\n{reg[0]}/{reg[1]}'

		return info


