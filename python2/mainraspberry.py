from tempsensor import TempSensor
from coapdtlsclient import coapDtlsClient
from coapthon import defines
from dtls.openssl import SSL_CIPHER_get_name, SSL_get_current_cipher
from uuid import getnode as get_mac
import time
from gpsSensor import GpsSensor
import sys
import logging.config
import string
import random
import globalvars

#global SSL time variables

logger = logging.getLogger(__name__)

def mountPayload(sensorId, sensorMac, temp, flow, gps, timestamp):
	payload = sensorId
	payload += '/'+sensorMac
	payload += '/'+temp
	payload += '/'+flow
	payload += '/'+gps
	payload += '/'+timestamp
	#print(payload)
	return payload

def getRealTemperature(temperatureSensor):
	return str(temperatureSensor.read_temp())

def getRealLocation(gps):
	return gps.getLatituteLongitudeAltitude()

def getFakeTemperature(temperatureSensor):
	return "25.2"

def getFakeLocation(gps):
	return "FixedLocation"


def randomString(stringLength):
    password_characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(password_characters) for i in range(stringLength))

if len(sys.argv) != 5 and len(sys.argv) != 4:
	print("Usage args [dtlstest or sensordtlstest or randomdtlstest] [cipherString] [numberOfRequisitons] [randomStringSize]")
	sys.exit()

randomStr = False

if sys.argv[1] == "dtlstest":
	getTemperature = getFakeTemperature
	getLocation = getFakeLocation
elif sys.argv[1] == "sensordtlstest":
	getTemperature = getRealTemperature
	getLocation = getRealLocation
elif sys.argv[1] == "randomdtlstest":
	getTemperature = getFakeTemperature
	getLocation = getFakeLocation
	randomStr = True
	randomStringSize = int(sys.argv[4])
else:
	sys.exit()

ciphers = sys.argv[2]
limitRequests = int(sys.argv[3])

#Temperature sensor file
temp_file = '/sys/bus/w1/devices/28-000004386422/w1_slave'

#Dtls coap client init
#host = "150.162.56.130"
#host = "192.168.25.6"
host = "34.95.217.89"
port = 5684

#RSA ca cert
caCertFile = "ca_cert.pem"
#ECDSA server key, server cert and ca cert
#caCertFile ="ca_ecdsa.crt"


clientDtls = coapDtlsClient(host, port, caCertFile, ciphers).client
#sensor init
temperatureSensor = TempSensor(temp_file)
gps = GpsSensor('/dev/ttyS0')

from dtls.openssl import *

try:
	tTotal = 0
	nRequests = 0

	#handshake measures
	while nRequests < limitRequests/10:
		tInicio = time.time()
		clientDtls.protocol._socket._sock.connect((host, port))
		tFim = time.time()
		tTotal += tFim - tInicio
		clientDtls.stop()
		clientDtls = coapDtlsClient(host, port, caCertFile, ciphers).client
		nRequests += 1

	clientDtls.protocol._socket._sock.connect((host, port))
	currentCipher = SSL_CIPHER_get_name(SSL_get_current_cipher(clientDtls.protocol._socket._sslobj._ssl.value))
	print("It took %f s, on cipher suite %s, to perform %f handshakes" % (tTotal, currentCipher, nRequests))
	
	globalvars.handshakeDone = True

	tTotal = 0
	nRequests = 0
	#CoAP post measure
	while nRequests < limitRequests:
		temperature =  getTemperature(temperatureSensor)
		position = getLocation(gps)
		macAddress = str(get_mac())
		timestamp = str(time.time())
		if randomStr:
			payload = randomString(randomStringSize)
		else:
			payload = mountPayload("SENSOR_JOHANN", macAddress, temperature, str(0), position, timestamp)
		try:
			tInicio = time.time()
			response = clientDtls.post("gpsflowtemp", payload, timeout=0, type = defines.Types["CON"])
			tFim = time.time()
			tTotal += tFim - tInicio
		except Exception as e:
			print("Post failed")
			print(e)
		try:
			pass
			#print(response.pretty_print())
		except Exception as e:
			pass
			#print("Mensagem nao chegou ao servidor")
		time.sleep(0.5)
		nRequests += 1
	currentCipher = SSL_CIPHER_get_name(SSL_get_current_cipher(clientDtls.protocol._socket._sslobj._ssl.value))
	print("It took %f s, on cipher suite %s, to send %f requests" % (tTotal, currentCipher, nRequests))
	if len(sys.argv) == 5:
		print("Each request payload was %f bytes" % randomStringSize)
	print("The total time of SSL_write() spent on POST operations was: %f" % globalvars.tSSLWrite)
	print("The total time of SSL_read() spent on responses reading was: %f" % globalvars.tSSLRead)
	print("\n\n")
	clientDtls.stop()
	sys.exit(0)
	#print "Best GPS read time: " + str(min(gpsTimes)) + " s"
	#print "Best temp read time: " + str(min(tempSensorTimes)) + " s"
except KeyboardInterrupt:
    print("cliente stopped")
    clientDtls.stop()
    print("Exiting...")
