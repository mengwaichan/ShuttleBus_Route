import csv
import airtag

class Airtags:
    def get_airtag(shuttleBus, prev_location):
        air_tag = []

        prev_address, prev_name = "", ""
        location = None
        if prev_location[shuttleBus]:
            prev_address = prev_location[shuttleBus].getAddress()
            prev_name = prev_location[shuttleBus].getName()

        with open("Airtags.csv", encoding="utf-8") as file:
            reader = csv.reader(file, delimiter=",")
            header = next(reader)

            for _, line in enumerate(reader):
                name = line[1]
                if name == shuttleBus:
                    streetAddress = line[6]
                    streetName = line[7]
                    if (streetAddress, streetName) != (prev_address, prev_name):
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
                    prev_address, prev_name = streetAddress, streetName
                    if location:
                        prev_location[shuttleBus] = location
                        
        if shuttleBus == "CCNY Shuttle 3":
            with open("Airtags.csv", "w", newline='', encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(header)

        return air_tag
