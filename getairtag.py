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
                latitude = line[4]
                longitude = line[5]
                if (latitude, longitude) != (prev_latitude, prev_longitude) or _ == 0:
                    air_tag.append(
                        airtag.AirTag(
                            dateTime = line[0],
                            name = line[1],
                            batteryStatus = line[2],
                            locationPostionType = line[3],
                            locationLatitude = line[4],
                            locationLongitude = line[5],
                            addressStreetAddress = line[6],
                            addressStreetName = line[7],
                            addressAreaOfInterestA = line[8],
                            addressAreaOfInterestB= line[9]
                    )
                    

                )
                prev_latitude, prev_longitude = latitude, longitude
        return air_tag
