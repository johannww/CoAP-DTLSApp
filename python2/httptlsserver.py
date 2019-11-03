# System
import socket
import random
import threading
import unittest
import tempfile
import os
import sys
from io import BytesIO

#HTTPS
import BaseHTTPServer, SimpleHTTPServer
import ssl

# Request handler (POST, GET, PUT, DELETE)
from coapdtlsrequesthandler import GpsFlowTempResource

# Logging
from logging import basicConfig, DEBUG, getLogger, root, Filter
basicConfig(level=DEBUG, format="%(asctime)s - %(threadName)-30s - %(name)s - %(levelname)s - %(message)s")

class HttpHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        print(body)

def main():
    #server = coapDtlsServer("0.0.0.0", 5684, "serverkey.pem", "ca_cert.pem").server;
    server = BaseHTTPServer.HTTPServer(('0.0.0.0', 443), HttpHandler)
    server.socket = ssl.wrap_socket(server.socket, certfile="serverkey.pem",ca_certs="ca_cert.pem", ciphers="ALL")
    while True:
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("Server Shutdown")
            print("Exiting...")
            server.shutdown()
            sys.exit(0)
        except Exception as e:
            print(e)

if __name__ == '__main__':
    main()
