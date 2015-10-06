
import serial
from time import sleep

class MyTurret:
	"""Wifi turret class"""
	def __init__(self, tty='/dev/ttyUSB0', timeout=10, 
			xlimits=[0, 180], ylimits=[0, 180],
			invertx=False, inverty=False, 
			step_deg=1, step_sec=0.05, 
			debug=1):
		self.debug = debug
		self.port=serial.Serial(port=tty, 
				baudrate=9600,
    				parity=serial.PARITY_ODD,
    				stopbits=serial.STOPBITS_TWO,
    				bytesize=serial.SEVENBITS,
				timeout=timeout)
		self.port.open()
		#self.port.write("test\n")
		#test=self.port.readline() #wait for initalizing
		#self.port.flushInput()
		self.inverty=inverty
		self.invertx=invertx
		self.step_deg = step_deg
		self.step_sec = step_sec
		for lim in (xlimits, ylimits):
			if (not (isinstance(lim, (list, tuple)) and (len(lim) == 2) \
					and all(isinstance(val, int) for val in lim))):
				raise ValueError('Limit must be a list of two integers')
			if (lim[0] < 0):
				raise ValueError('Low limit cannot be less than 0')
			if (lim[1] > 180):
				raise ValueError('High limit cannot be more than 180')
		self.limits = {'x': xlimits, 'y': ylimits}
		# Set ping timeout as 1/5 of main timeout, 
		# but not less than 1 sec.
		# By default, 10/5 = 2 sec.
		# Float timeout values is allowed by pyserial.
		self.ping_timeout = max(timeout/5.0, 1)
		# Wait for initializing
		while (not self.ping()):
			sleep(0.5)


	def __del__(self):
		self.finish()

	def finish(self):
		self.port.close()
	
	def ping(self):
		old_timeout = self.port.timeout
		self.port.timeout = self.ping_timeout
		if (self.debug):
			print('Pinging...')
		self.port.write('test\n')
		out = self.port.readline().rstrip()
		if (self.debug):
			print('Got answer: "{:s}"'.format(out) \
					if out else 'Timeout!')
		self.port.timeout = old_timeout
		if (out == 'OK'):
			return True
		return False

	def invert(self,var):
		return (180 - var)

	def sety(self,newy):
		newy = int(newy)
		if self.inverty: 
			newy=self.invert(newy)
		if (self.limits['y'][0] <= newy <= self.limits['y'][1]):
			self.port.write('sy{:d}\n'.format(newy))
		else:
			raise ValueError(('Cannot set y = {:d} because value ' + 
				'is out of allowed range [{:d}:{:d}]').\
				format(newy, self.limits['y'][0], self.limits['y'][1]))
		
	def setx(self,newx):
		newx = int(newx)
		if self.invertx: 
			newy=self.invert(newx)
		if (self.limits['x'][0] <= newx <= self.limits['x'][1]):
			self.port.write('sx{:d}\n'.format(newx))
		else:
			raise ValueError(('Cannot set x = {:d} because value '
				'is out of allowed range [{:d}:{:d}]').\
				format(newx, self.limits['x'][0], self.limits['x'][1]))
	
	def slowly(self, coord, newval):
		newval = int(newval)
		if (coord == 'x'):
			oldval = self.getx()
			if self.invertx:
				newval = self.invert(newval)
		elif (coord == 'y'):
			oldval = self.gety()
			if self.inverty:
				newval = self.invert(newval)
		else:
			raise ValueError('Value for coord must be "x" or "y", but "{:s}" given'.\
					format(str(coord)))
		if (not (0 <= newval <= 180)):
			raise ValueError('New value {:s} = {:d} not in range 0..180'.\
					format(coord, newval))
		if (newval > oldval):
			step = self.step_deg
		elif (newval < oldval):
			step = -self.step_deg
		elif (newval == oldval):
			# We're already happy
			return
		else:
			# Such situation is possible if one of values is NaN,
			# but integer cannot be NaN!
			# None is less than any integer, it's clear in that way
			raise ZeroDivisionError("Wat da fuck?")
		# Guarantee that last value will be newval
		for it in range(oldval + step, newval, step) + [newval]:
			if (self.debug):
				print("Set {:1s}={:3d}".format(coord, it))
			self.port.write('s{:s}{:d}\n'.format(coord, it))
			sleep(self.step_sec)
	
	# For those who prefers to use non-generic methods
	# This
	def setx_slow(self, newx):
		self.slowly('x', newx)

	# And that
	def sety_slow(self, newy):
		self.slowly('y', newy)

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

