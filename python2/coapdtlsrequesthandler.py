from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource
from dbhandler import DataBase
import time
 
class GpsFlowTempResource(Resource):
    def __init__(self, name="gpsflowtemp", coap_server=None):
        super(GpsFlowTempResource, self).__init__(name, coap_server, visible=True,
                                            observable=True, allow_children=True)
        self.payload = None
        #self.dbhandler = DataBase()
        #self.dbhandler.connect_db()
        self.timeUsedToPerform = 0
        self.nPosts = 0
 
    def render_GET(self, request):
        return self
 
    def render_PUT(self, request):
        return self
 
    def render_POST(self, request):
        #res = self.init_resource(request, GpsFlowTempResource())
        tInicio = time.time()
        res = self.init_resource(request, self)
        res.location_query = request.uri_query
        res.payload = request.payload
        print(request.source)
        print("\n"+res.payload)
        #self.dbhandler.on_message(request.payload)
        tFim = time.time()
        self.timeUsedToPerform += tFim - tInicio
        self.nPosts += 1
        return res
 
    def render_DELETE(self, request):
        return True

    def getProcessTimeUsed(self):
        return self.timeUsedToPerform