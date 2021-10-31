from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Table
w, h = A4

def makeReport(host):
	c = canvas.Canvas(f'{host.ip} report.pdf')

	c.drawImage(f'{host.monitor.systemGet(host.ip)}.jpg', 50, h - 300, width = 500, height = 250)
	text = c.beginText(50, h - 350)

	content = str(host.monitor.snmpConsult(host.ip, '1.3.6.1.2.1.1.1.0'))
	if len(content) > 80:
		content = [content[:80], content[80:]]
		text.textLines('\n'.join(content))
	else:
		text.textLine(content)
		
	content = host.monitor.snmpConsult(host.ip, '1.3.6.1.2.1.1.6.0')
	text.textLines(f'\n\nLocalizacion: {content}')

	content = host.monitor.snmpConsult(host.ip, '1.3.6.1.2.1.2.1.0')
	text.textLines(f'\n\nNumero de interfaces: {content}')

	content = int(host.monitor.snmpConsult(host.ip, '1.3.6.1.2.1.1.3.0'))/360000
	text.textLines(f'\n\nTiempo desde ultimo reinicio (horas): {content}')

	text.textLines(f'Comunidad: {host.monitor.comunity}')
	text.textLines(f'IP: {host.ip}')
	text.textLines(f'Nivel de uso: {host.ulvlname()}')

	text.setFont('Times-Roman', 12)
	c.drawText(text)

	costs = host.costtable()

	xyText(c, 50, h/2 - 70, 'Usage Type')
	xyText(c, 50+100, h/2 - 70, f'Usage')
	xyText(c, 50+300, h/2 - 70, f'Cost')

	xyText(c, 50, h/2 - 100, costs[0][0])
	xyText(c, 50+100, h/2 - 100, f'{costs[0][1]}')
	xyText(c, 50+300, h/2 - 100, f'${costs[0][4]}')
	xyText(c, 50, h/2 - 120, f'{costs[0][2]} | {costs[0][3]}')

	if len(costs) >= 2:
		xyText(c, 50, h/2 - 150, costs[1][0])
		xyText(c, 50+100, h/2 - 150, f'{costs[1][1]}')
		xyText(c, 50+300, h/2 - 150, f'${costs[1][4]}')
		xyText(c, 50, h/2 - 170, f'{costs[1][2]} | {costs[1][3]}')
		xyText(c, 50, h/2 - 200, f'Total: ${costs[0][4] + costs[1][4]}')
	else:
		xyText(c, 50, h/2 - 150, f'Total: ${costs[0][4]}')

	c.showPage()

	c.save()

def xyText(c, x, y, text):
	t = c.beginText(x, y)
	t.textLine(text)
	c.drawText(t)

if __name__ == '__main__':
	from SNMPdata import MonitorInfo
	m = MonitorInfo(hosts = ['localhost'])
	tar = 'localhost'
	makeReport(m, tar)