
import serial,time

class MyTurret:
	"""Wifi turret class"""
	def __init__(self,tty='/dev/ttyUSB0',timeout=10):
		self.port=serial.Serial(port=tty, 
				baudrate=9600,
    				parity=serial.PARITY_ODD,
    				stopbits=serial.STOPBITS_TWO,
    				bytesize=serial.SEVENBITS,
				timeout=timeout)
		self.port.open()
		time.sleep(2)

	def __del__(self):
		self.finish()

	def finish(self):
		self.port.close()

	def sety(self,newy):
		if not (int(newy) < 0 or int(newy) > 180):
			self.port.write('sy'+str(newy)+'\n')
		else:
			print "ERROR! Y not in range 0..180 Not moving"
		
	def setx(self,newx):
		if not (int(newx) < 0 or int(newx) > 180):
			self.port.write('sx'+str(newx)+'\n')
		else:
			print "ERROR! X not in range 0..180 Not moving"

	def gety(self):
		self.port.write('gy\n')
		time.sleep(1)
		out=''
		while self.port.inWaiting() > 0:
			out += self.port.read(1)
		return out
	
	def getx(self):
		self.port.write('gx\n')
		time.sleep(1)
		out=''
		while self.port.inWaiting() > 0:
			out += self.port.read(1)
		return out

