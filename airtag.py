import csv
import airtag

class AirTag:
    def __init__(self,
                 dateTime,
                 name,
                 serialNumber,
                 productType,
                 productIndentifier,
                 vendorIdentifier,
                 antennaPower,
                 systemVersion,
                 batteryStatus,
                 locationPostionType,
                 locationLatitude,
                 locationLongitude,
                 locationTimestamp,
                 locationVerticalAccuracy,
                 locationHorizontalAccuracy,
                 locationFloorLevel,
                 locationAltitude,
                 locationIsInAccurate,
                 locationIsOld,
                 locationFinished,
                 addressLabel,
                 addressStreetAddress,
                 addressCountryCode,
                 addressStateCode,
                 addressAdministrativeArea,
                 addressStreetName,
                 addressLocality,
                 addressCountry,
                 addressAreaOfInterestA,
                 addressAreaOfInterestB):
        self.dateTime = dateTime
        self.name = name
        self.serialNumber = serialNumber
        self.productType = productType
        self.productIndentifier = productIndentifier
        self.vendorIdentifier = vendorIdentifier
        self.antennaPower = antennaPower
        self.systemVersion = systemVersion
        self.batteryStatus = batteryStatus
        self.locationPostionType = locationPostionType
        self.locationLatitude = locationLatitude
        self.locationLongitude = locationLongitude
        self.locationTimestamp = locationTimestamp
        self.locationVerticalAccuracy = locationVerticalAccuracy
        self.locationHorizontalAccuracy = locationHorizontalAccuracy
        self.locationFloorLevel = locationFloorLevel
        self.locationAltitude = locationAltitude
        self.locationIsInAccurate = locationIsInAccurate
        self.locationIsOld = locationIsOld
        self.locationFinished = locationFinished
        self.addressLabel = addressLabel
        self.addressStreetAddress = addressStreetAddress
        self.addressCountryCode = addressCountryCode
        self.addressStateCode = addressStateCode
        self.addressAdministrativeArea = addressAdministrativeArea
        self.addressStreetName = addressStreetName
        self.addressLocality = addressLocality
        self.addressCountry = addressCountry
        self.addressAreaOfInterestA = addressAreaOfInterestA
        self.addressAreaOfInterestB = addressAreaOfInterestB
    
    def to_json(self):
        return{
            "datetime":self.dateTime,
            "name":self.name,
            "serialnumber":self.serialNumber,
            "lat" :self.locationLatitude,
            "lng" :self.locationLongitude,
            "streetAddress" : self.addressStreetAddress,
            "streetName" : self.addressStreetName
            }
