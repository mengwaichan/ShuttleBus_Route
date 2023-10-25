class BusStop:
    def __init__(self, stopID, stopName, stopLat, stopLng, streetaddressname = None, streetaddress = None):
        self.stopID = stopID
        self.stopName = stopName
        self.stopLat = stopLat
        self.stopLng = stopLng
        self.streetaddressname = streetaddressname
        self.streetaddress = streetaddress
    
    def getStop(self):
        return [self.stopLat, self.stopLng]

w145 = BusStop(1, "W 145", 40.82377614314247, -73.94502568555461, 691, "St Nicholas Ave") #691 St Nicholas Ave
nac = BusStop(2, "NAC", 40.819557163853155, -73.94991793531442, 201, "Convent Ave") # 201 The City College of New York
w125 = BusStop(3, "W 125", 40.8103721597239, -73.95278450679731, 284, "St Nicholas Ave") # 284 St Nicholas Ave # W 124th St
intermediate = BusStop(4, "intermediate", 40.810976077358795, -73.95405670678701)
