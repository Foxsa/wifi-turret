
import serial

class MyTurret:
	"""Wifi turret class"""
	def __init__(self,tty='/dev/ttyUSB0',timeout=10,invertx=False,inverty=False):
		self.port=serial.Serial(port=tty, 
				baudrate=9600,
    				parity=serial.PARITY_ODD,
    				stopbits=serial.STOPBITS_TWO,
    				bytesize=serial.SEVENBITS,
				timeout=timeout)
		self.port.open()
		#self.port.write("test\n")
		test=self.port.readline() #wait for initalizing
		self.port.flushInput()
		self.inverty=inverty
		self.invertx=invertx

	def __del__(self):
		self.finish()

	def finish(self):
		self.port.close()

	def invert(self,var):
		return -1*(var-180)

	def sety(self,newy):
		if self.inverty: 
			newy=self.invert(newy)
		if not (int(newy) < 0 or int(newy) > 180):
			self.port.write('sy'+str(newy)+'\n')
		else:
			print "ERROR! Y not in range 0..180 Not moving"
		
	def setx(self,newx):
		if self.invertx: 
			newy=self.invert(newx)
		if not (int(newx) < 0 or int(newx) > 180):
			self.port.write('sx'+str(newx)+'\n')
		else:
			print "ERROR! X not in range 0..180 Not moving"
	def aim(self,options):
		self.setx(options['x'])
		self.sety(options['y'])

	def gety(self):
		self.port.write('gy\n')
		out=self.port.readline()
		return int(out)
	
	def getx(self):
		self.port.write('gx\n')
		out=self.port.readline()
		return int(out)

