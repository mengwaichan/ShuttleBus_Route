import csv
import airtag

class Airtags:
    def get_airtag():
        air_tag = []

        prev_latitude, prev_longitude = None, None

        with open("Airtags.csv", encoding="utf-8") as file:
            reader = csv.reader(file, delimiter=",")
            next(reader)

            for _, line in enumerate(reader):
                latitude = line[10]
                longitude = line[11]
                if (latitude, longitude) != (prev_latitude, prev_longitude) or _ == 0:
                    air_tag.append(
                        airtag.AirTag(
                            dateTime = line[0],
                            name = line[1],
                            serialNumber = line[2],
                            productType = line[3],
                            productIndentifier = line[4],
                            vendorIdentifier = line[5],
                            antennaPower = line[6],
                            systemVersion = line[7],
                            batteryStatus = line[8],
                            locationPostionType = line[9],
                            locationLatitude = line[10],
                            locationLongitude = line[11],
                            locationTimestamp = line[12],
                            locationVerticalAccuracy = line[13],
                            locationHorizontalAccuracy = line[14],
                            locationFloorLevel = line[15],
                            locationAltitude = line[16],
                            locationIsInAccurate = line[17],
                            locationIsOld = line[18],
                            locationFinished = line[19],
                            addressLabel = line[20],
                            addressStreetAddress = line[21],
                            addressCountryCode = line[22],
                            addressStateCode = line[23],
                            addressAdministrativeArea = line[24],
                            addressStreetName = line[25],
                            addressLocality = line[26],
                            addressCountry = line[27],
                            addressAreaOfInterestA = line[28],
                            addressAreaOfInterestB= line[29]
                    )
                    

                )
                prev_latitude, prev_longitude = latitude, longitude
        return air_tag
