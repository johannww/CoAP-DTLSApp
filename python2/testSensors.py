import os
import time
from tempsensor import TempSensor
from gpsSensor import GpsSensor
import timeit
import functools

temp_file = '/sys/bus/w1/devices/28-000004386422/w1_slave'

temperatureSensor = TempSensor(temp_file);
gps = GpsSensor('/dev/ttyS0')
numberOfReads = 300

gpsSensorTime = (timeit.Timer(functools.partial(gps.getLatituteLongitudeAltitude)).timeit(numberOfReads))
tempSensorTime = (timeit.Timer(functools.partial(temperatureSensor.read_temp)).timeit(numberOfReads))

print "GPS sensor took " + str(gpsSensorTime) + " seconds to perform " + str(numberOfReads) + " reads"
print "GPS sensor took " + str(tempSensorTime) + " seconds to perform " + str(numberOfReads) + " reads"
