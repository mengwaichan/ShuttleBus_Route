import busStop
from route import Route

w145 = busStop.BusStop(1, "W145", 40.82377614314247, -73.94502568555461, 691, "St Nicholas Ave") #691 St Nicholas Ave
nac = busStop.BusStop(2, "NAC", 40.819557163853155, -73.94991793531442, 201, "Convent Ave") # 201 The City College of New York
w125 = busStop.BusStop(3, "W125", 40.8103721597239, -73.95278450679731, 284, "St Nicholas Ave") # 284 St Nicholas Ave # W 124th St
intermediate = busStop.BusStop(4, "intermediate", 40.810976077358795, -73.95405670678701)

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
        self.nextStop = None
        self.intermediate = None

    def fetchRoute(self):
        bus_route = Route()

        destlat = self.nextStop.getLat()
        destlng = self.nextStop.getLng()


        response_data = bus_route.getRoute(self.lat, self.lng, destlat, destlng)

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
            self.nextStop = nac
            return
        if int(self.streetaddress) < 210 and self.streetname == "Convent Ave": # CCNY
            if self.w145: # going to w125
                self.nextStop = w125
                self.intermediate = intermediate
                return
            else: # going to w145
                self.nextStop = w145
                return
        if int(self.streetaddress) <= 300 and self.streetname == "St Nicholas Ave": #125
            self.w145 = False
            self.w125 = True
            self.nextStop = nac
            return
        
    def getLastDest(self, route):
        self.nextStop = route.nextStop
        self.intermediate = route.intermediate

    def to_json(self):
        stop = self.nextStop.getName()
        return {
            "datetime":self.datetime,
            "name":self.name,
            "serialnumber":self.serialnumber,
            "lat" :self.lat,
            "lng" :self.lng,
            "streetAddress" : self.streetaddress,
            "streetName" : self.streetname,
            "distance" : self.distance,
            "duration" : self.duration,
            "nextStop" : stop
        }
