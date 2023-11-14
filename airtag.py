import csv
import airtag

# To-do
# Remove get() methods
class AirTag:
    def __init__(self,
                 dateTime,
                 name,
                 batteryStatus,
                 locationPostionType,
                 locationLatitude,
                 locationLongitude,
                 addressStreetAddress,
                 addressStreetName,
                 addressAreaOfInterestA,
                 addressAreaOfInterestB):
        self.dateTime = dateTime
        self.name = name
        self.batteryStatus = batteryStatus
        self.locationPostionType = locationPostionType
        self.locationLatitude = locationLatitude
        self.locationLongitude = locationLongitude
        self.addressStreetAddress = addressStreetAddress
        self.addressStreetName = addressStreetName
        self.addressAreaOfInterestA = addressAreaOfInterestA
        self.addressAreaOfInterestB = addressAreaOfInterestB
    
    def toJson(self):
        return{
            "datetime":self.dateTime,
            "name":self.name,
            "lat" :self.locationLatitude,
            "lng" :self.locationLongitude,
            "streetAddress" : self.addressStreetAddress,
            "streetName" : self.addressStreetName
            }
    def getName(self):
        return self.addressStreetName
    def getAddress(self):
        return self.addressStreetAddress
