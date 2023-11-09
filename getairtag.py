import csv
import airtag

class Airtags:
    def get_airtag(shuttleBus, prev_location):
        air_tag = []

        prev_latitude, prev_longitude = None, None
        location = None
        if prev_location[shuttleBus]:
            prev_latitude = prev_location[shuttleBus].getLat()
            prev_longitude = prev_location[shuttleBus].getLng()
            print(prev_latitude, prev_longitude, prev_location[shuttleBus].name)

        with open("Airtags.csv", encoding="utf-8") as file:
            reader = csv.reader(file, delimiter=",")
            header = next(reader)

            for _, line in enumerate(reader):
                name = line[1]
                if name == shuttleBus:
                    latitude = line[4]
                    longitude = line[5]
                    if (latitude, longitude) != (prev_latitude, prev_longitude) or _ == 0:
                        location = airtag.AirTag(
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
                        air_tag.append(location)
                    prev_latitude, prev_longitude = latitude, longitude
                    if location:
                        prev_location[shuttleBus] = location
        if shuttleBus == "CCNY Shuttle 3":
            with open("Airtags.csv", "w", newline='', encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(header)

        return air_tag
