import busStop
from route import Route
from geocoding import Geocoding

# To-do
# Make this code more modular
# Improve getNextStop() Method
# Error handling needs to be added
# BusStop changed to constants
# 
# Use Flask to build an API to add, delete, or restrict bus stops


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
        self.nextStop = None
        self.intermediate = None
        self.prevStop = None

        self.prevRoute = None

    # Set previous route data
    def setPrev(self, prev = None):
        self.prevRoute = prev
        if prev:
            self.prevStop = prev.prevStop

    # Retrieve Route from route.py using Google MAP API
    def fetchRoute(self):
        busRoute = Route()

        destlat = self.nextStop.stopLat
        destlng = self.nextStop.stopLng

        if self.intermediate:
            interlat = self.intermediate.stopLat
            interlng = self.intermediate.stopLng
            responseData = busRoute.fetchRoute(self.lat, self.lng, destlat, destlng, interlat, interlng)
        else:
            responseData = busRoute.fetchRoute(self.lat, self.lng, destlat, destlng)

        try:
            self.distance = responseData['routes'][0]['distanceMeters']
        except (KeyError, IndexError):
            self.distance = None

        try:
            self.duration = responseData['routes'][0]['duration']
        except (KeyError, IndexError):
            self.duration = None

        try:
            self.polyline = responseData['routes'][0]['polyline']['encodedPolyline']
        except (KeyError, IndexError):
            self.polyline = None

    # Determine Bus Next Stop
    def getNextStop(self):
        self.cleanData()
        self.adjustOrigin()
        if not self.prevStop:
            self.prevStop == nac

        # Reached busStop
        if (int(self.streetaddress) >= 630 and self.streetname == "St Nicholas Ave") or self.streetname == "W 145th St" or self.streetname == "W 141st St" or (self.interestA == "145 St" and self.streetaddress == ""): #145
            self.nextStop = nac
            self.prevStop = w145
            return
        
        if ((150 <= int(self.streetaddress) <= 210)  and self.streetname == "Convent Ave") or (self.interestA == "The City College of New York" and self.streetaddress == ""): # CCNY
            if self.prevStop == w125: # going to w145
                self.nextStop = w145
                self.prevStop = nac
                return
            elif self.prevStop == w145: # going to w125
                self.nextStop = w125
                self.intermediate = intermediate_to_125
                self.prevStop = nac
                return
       
        if (100 <= int(self.streetaddress) <= 300 and self.streetname == "St Nicholas Ave") or self.streetname == "Hancock Pl" or (self.streetname == "W 125th St" and int(self.streetaddress) < 400) or self.streetname == "W 124th St" or self.streetname == "Manhattan Ave": #125
            self.nextStop = nac
            self.intermediate = intermediate_to_nac
            self.prevStop = w125
            return
        
        if 0 == int(self.streetaddress) and self.streetname == "St Nicholas Ave":
            if self.interestA == "125 St":
                self.nextStop = nac
                self.intermediate = intermediate_to_nac
                self.prevStop = w125
                return
            else:
                self.nextStop = nac
                self.prevStop = w145
                return
        

    
        if self.prevRoute:
            self.skippedStop()
            return
    
    def skippedStop(self):
        if (210 < int(self.streetaddress) <= 355 and self.streetname == "Convent Ave") and self.prevRoute.prevStop == w125:
            self.nextStop = w145
            self.prevStop = nac
            return
        if ((135 >= int(self.streetaddress) and self.streetname == "Convent Ave") or self.streetname == "Morningside Ave" ) and self.prevRoute.prevStop == w145 :
            self.nextStop = w125
            self.prevStop = nac
            return
        
    # If Airtag Location is slightly off the route, Re-adjust the location
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
        if self.streetname == "St Nicholas Terr" and int(self.streetaddress) > 250 or self.streetname == "W 140th St":
            self.lat = 40.81991080221068
            self.lng = -73.94967653138818
            self.streetname = "Convent Ave"
            self.streetaddress = 255
            return

    # Handlde any NULL values, and String on streetaddress within the data collected
    def cleanData(self):
        if not self.streetaddress or self.streetaddress == ' ':
            self.streetaddress = 0
        if not self.streetname or self.streetname == ' ':
            self.streetname = ""
        if type(self.streetaddress) == str and "–" in self.streetaddress:
            self.streetaddress = int(self.streetaddress.split('–')[0])

    # Retreive the Last Location the bus was headed
    def getLastDest(self):
        if not self.prevRoute:
            self.nextStop = nac
            return
        self.nextStop = self.prevRoute.nextStop
        self.intermediate = self.prevRoute.intermediate

    # Clear any Intermediate On the route that is not suppose to be on
    def deleteIntermediate(self):
        if (int(self.streetaddress) <= 300 and self.streetname == "St Nicholas Ave") or self.streetname == "Hancock Pl" or self.streetname == "W 125th St" or self.streetname == "W 124th St":
            self.intermediate = None

    # Return Json Format of this object
    def toJson(self):
        return {
            "datetime":self.datetime,
            "name":self.name,
            "lat" :self.lat,
            "lng" :self.lng,
            "streetAddress" : self.streetaddress,
            "streetName" : self.streetname,
            "distance" : self.distance,
            "duration" : self.duration,
            "nextStop" : self.nextStop.stopName,
            "polyline" : self.polyline
        }
    