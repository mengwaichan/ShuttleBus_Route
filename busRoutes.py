import busStop
from route import Route
from geocoding import Geocoding

w145 = busStop.BusStop(1, "W145", 40.82377614314247, -73.94502568555461, 691, "St Nicholas Ave") #691 St Nicholas Ave
nac = busStop.BusStop(2, "NAC", 40.819557163853155, -73.94991793531442, 201, "Convent Ave") # 201 The City College of New York
w125 = busStop.BusStop(3, "W125", 40.8103721597239, -73.95278450679731, 284, "St Nicholas Ave") # 284 St Nicholas Ave # W 124th St
intermediate_to_125 = busStop.BusStop(4, "intermediate_125", 40.810976077358795, -73.95405670678701)
intermediate_to_nac = busStop.BusStop(5, "intermediate_nac", 40.811255, -73.953659)

class BusRoutes:
    def __init__(self, datetime, name, lat, lng, streetaddress, streetname, interestA):

        # Data from Airtags
        self.datetime = datetime
        self.name = name
        self.lat = lat
        self.lng = lng
        self.streetaddress = streetaddress
        self.streetname = streetname
        self.interestA = interestA

        # Data from Google Route API
        self.distance = None
        self.duration = None
        self.polyline = None

        # Determine Bus Direction
        self.w125 = False # if true it passed w125, false is heading to w125
        self.w145 = False 
        self.nextStop = None
        self.intermediate = None

    def fetchRoute(self):
        bus_route = Route()

        destlat = self.nextStop.getLat()
        destlng = self.nextStop.getLng()

        if self.intermediate:
            interlat = self.intermediate.getLat()
            interlng = self.intermediate.getLng()
            response_data = bus_route.getRoute(self.lat, self.lng, destlat, destlng, interlat, interlng)
        else:
            response_data = bus_route.getRoute(self.lat, self.lng, destlat, destlng)

        try:
            self.distance = response_data['routes'][0]['distanceMeters']
        except (KeyError, IndexError):
            self.distance = None

        try:
            self.duration = response_data['routes'][0]['duration']
        except (KeyError, IndexError):
            self.duration = None

        try:
            self.polyline = response_data['routes'][0]['polyline']['encodedPolyline']
        except (KeyError, IndexError):
            self.polyline = None

    def get_nextStop(self, prev = None):
        self.checkData()
        self.adjustOrigin()
          
        if prev:
            self.w145 = prev.w145
            self.w125 = prev.w125

        if (int(self.streetaddress) >= 630 and self.streetname == "St Nicholas Ave") or (self.streetname == "W 145th St" and 410 < int(self.streetaddress)) or self.streetname == "W 141st St": #145
            self.w145 = True
            self.w125 = False
            self.nextStop = nac
            return
        if  (int(self.streetaddress) == 0 or 150 <= int(self.streetaddress) <= 250)  and self.streetname == "Convent Ave": # CCNY
            if self.w145: # going to w125
                self.nextStop = w125
                self.intermediate = intermediate_to_125
                return
            else: # going to w145
                self.nextStop = w145
                return
        if (int(self.streetaddress) <= 300 and self.streetname == "St Nicholas Ave") or self.streetname == "Hancock Pl" or (self.streetname == "W 125th St" and int(self.streetaddress) < 400) or self.streetname == "W 124th St" or self.streetname == "Manhattan Ave": #125
            self.w145 = False
            self.w125 = True
            self.nextStop = nac
            self.intermediate = intermediate_to_nac
            return
        if self.interestA == "The City College of New York" and self.streetaddress == "":
            if self.w145: # going to w125
                self.nextStop = w125
                self.intermediate = intermediate_to_125
                return
            else: # going to w145
                self.nextStop = w145
                return
    
    def adjustOrigin(self):
        if self.streetname == "Hamilton Terr":
            self.lat = 40.821713 
            self.lng = -73.947070
            self.streetname = "W 141st St"
            self.streetaddress = 428
            return
        if self.streetname == "Amsterdam Ave" and 1510 <= int(self.streetaddress) <= 1617:
            self.lat = 40.8198374
            self.lng = -73.9505743
            self.streetname = "Convnet Ave"
            self.streetaddress = 160
            return
        if self.streetname == "Amsterdam Ave" and 1360 < int(self.streetaddress) < 1510:
            newCord = Geocoding()
            res = newCord.fetchLatLng(int(self.streetaddress) - 1360, "Convnet Ave")
            self.lat = res['lat']
            self.lng = res['lng']
            self.streetname = "Convnet Ave"
            self.streetaddress = int(self.streetaddress) - 1360
            return

    def checkData(self):
        if not self.streetaddress or self.streetaddress == ' ':
            self.streetaddress = 0
        if not self.streetname or self.streetname == ' ':
            self.streetname = ""
        if type(self.streetaddress) == str and "–" in self.streetaddress:
            self.streetaddress = int(self.streetaddress.split('–')[0])

    def getLastDest(self, route = None):
        if not route:
            return
        self.nextStop = route.nextStop
        self.intermediate = route.intermediate

    def deleteIntermediate(self):
        if (int(self.streetaddress) <= 300 and self.streetname == "St Nicholas Ave") or self.streetname == "Hancock Pl" or self.streetname == "W 125th St" or self.streetname == "W 124th St":
            self.intermediate = None

    def to_json(self):
        return {
            "datetime":self.datetime,
            "name":self.name,
            "lat" :self.lat,
            "lng" :self.lng,
            "streetAddress" : self.streetaddress,
            "streetName" : self.streetname,
            "distance" : self.distance,
            "duration" : self.duration,
            "nextStop" : self.nextStop.getName(),
            "polyline" : self.polyline
        }
    