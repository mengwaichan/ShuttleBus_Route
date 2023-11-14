# To-do
# Remove get functions

class BusStop:
    def __init__(self, stopID, stopName, stopLat, stopLng, streetaddressname = None, streetaddress = None):
        self.stopID = stopID
        self.stopName = stopName
        self.stopLat = stopLat
        self.stopLng = stopLng
        self.streetaddressname = streetaddressname
        self.streetaddress = streetaddress
    
    def getLat(self):
        return self.stopLat
    def getLng(self):
        return self.stopLng
    def getName(self):
        return self.stopName
