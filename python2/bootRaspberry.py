from coapdtlsclient import coapDtlsClient
from uuid import getnode as get_mac
import urllib2
import sys

def wait_for_internet_connection():
    while True:
        try:
            response = urllib2.urlopen('http://google.com',timeout=1)
            return
        except urllib2.URLError:
            pass

ciphers = "ECDHE+AESGCM"

wait_for_internet_connection()

clienteDtls = coapDtlsClient("34.95.217.89", 5684, "/home/pi/app2/ca_cert.pem", ciphers).client

try:
	macAddress = str(get_mac())
	response = clienteDtls.post("gpsflowtemp", macAddress, timeout=7)
	try:
		print response.pretty_print()
	except Exception as e:
		print "Mensagem nao chegou ao servidor"
	clienteDtls.stop()
	sys.exit()
except KeyboardInterrupt:
    print "cliente stopped"
    clienteDtls.stop()
    print "Exiting..."