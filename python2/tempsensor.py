import os
import time

#os.system('modprobe w1-gpio')
#os.system('modprobe w1-therm')
#temp_file = '/sys/bus/w1/devices/28-0317030bf2ff/w1_slave'

class TempSensor(object):
    def __init__(self, temp_file):
        super(TempSensor, self).__init__()
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')
        self.temp_file = temp_file
                        
    def read_temp_file(self):
        f = open(self.temp_file, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def read_temp(self):
        lines = self.read_temp_file()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.1)
            lines = self.read_temp_file()
        temp_output = lines[1].find('t=')
        if temp_output == -1:
            return -1
        temp_string = lines[1].strip()[temp_output+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

