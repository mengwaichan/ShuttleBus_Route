import busStop
from route import Route

class BusRoutes:
    def __init__(self, datetime, name, serialnumber, lat, lng, streetaddress, streetname):
        self.datetime = datetime
        self.name = name
        self.serialnumber = serialnumber
        self.lat = lat
        self.lng = lng
        self.streetaddress = streetaddress
        self.streetname = streetname
        self.distance = None
        self.duration = None
        self.w125 = False # if true it passed w125, false is heading to w125
        self.w145 = False 
        self.destlat = busStop.nac.stopLat
        self.destlng = busStop.nac.stopLng
        self.interlat = None
        self.interlng = None

    def fetchRoute(self):
        bus_route = Route()

        response_data = bus_route.getRoute(self.lat, self.lng, self.destlat, self.destlng)

        self.distance = response_data['routes'][0]['distanceMeters'] 
        self.duration = response_data['routes'][0]['duration']

    def get_nextStop(self):
        if not self.streetaddress:
            self.streetaddress = 0
        if not self.streetname:
            self.streetname = ""

        if int(self.streetaddress) >= 690 and self.streetname == "St Nicholas Ave": #145
            self.w145 = True
            self.w125 = False
            self.destlat = busStop.nac.stopLat
            self.destlng = busStop.nac.stopLng
            return
        if int(self.streetaddress) < 210 and self.streetname == "Convent Ave": # CCNY
            if self.w145: # going to w125
                self.destlat = busStop.w125.stopLat
                self.destlng = busStop.w125.stopLng
                self.interlat = busStop.intermediate.stopLat
                self.interlng = busStop.intermediate.stopLng
                return
            else: # going to w145
                self.destlat = busStop.w145.stopLat
                self.destlng = busStop.w145.stopLng
                return
        if int(self.streetaddress) <= 300 and self.streetname == "St Nicholas Ave": #125
            self.w145 = False
            self.w125 = True
            self.destlat = busStop.nac.stopLat
            self.destlng = busStop.nac.stopLng
            return
        
    def setdest(self, destlat, destlng, interlat, interlng):
        self.destat = destlat
        self.destlng = destlng
        self.interlat = interlat
        self.interlng = interlng   
    
    def to_json(self):
        return {
            "datetime":self.datetime,
            "name":self.name,
            "serialnumber":self.serialnumber,
            "lat" :self.lat,
            "lng" :self.lng,
            "streetAddress" : self.streetaddress,
            "streetName" : self.streetname,
            "distance" : self.distance,
            "duration" : self.duration
        }