#read pySerial

import serial
import signal
import time

def timeout(arg1, arg2):
	raise Exception('GPS timelimit exceeded')

class GpsSensor(object):
	"""docstring for GpsSensor"""
	def __init__(self, serialInterface):
		super (GpsSensor, self).__init__()
		#self.ser = serial.Serial(self.serialInterface, 9600, timeout=1)
		self.ser = serial.Serial()
		self.ser.port = serialInterface
		self.ser.baudrate = 9600
		self.ser.timeout = 1
		signal.signal(signal.SIGALRM, timeout)

	def getLatituteLongitudeAltitude(self):
		try:
			return self.findLatittudeLongitudeAltitudeSerial()
		except serial.SerialException as e:
			signal.alarm(0)
			self.ser.close()
			print(e)
			print("Serial unavailable")
			return str()
		except Exception as e:
			signal.alarm(0)
			self.ser.close()
			print(e)
			print("GPS could not be read in time!")
			return str()

	def findLatittudeLongitudeAltitudeSerial(self):
		signal.alarm(5)
		self.ser.open()
		line = str()
		while line[0:6] != "$GPRMC":
			#print(line[0:6])
			line = self.ser.readline()
		signal.alarm(0)
		self.ser.close()
		return line
