import csv

# Airtag object 
class AirTag:
    def __init__(self,
                 datetime,
                 name,
                 battery_status,
                 position_type,
                 latitude,
                 longitude,
                 street_address,
                 street_name,
                 area_of_interest_a,
                 area_of_interest_b):
        self.datetime = datetime
        self.name = name
        self.battery_status = battery_status
        self.position_type = position_type
        self.latitude = latitude
        self.longitude = longitude
        self.street_address = street_address
        self.street_name = street_name
        self.area_of_interest_a = area_of_interest_a
        self.area_of_interest_b = area_of_interest_b
    
    def to_json(self):
        return {
            "datetime": self.datetime,
            "name": self.name,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "streetAddress": self.street_address,
            "streetName": self.street_name
        }

"""
Retrieve unique Airtag data points for a specific shuttle bus.

Args:
    shuttle_bus (str): Name of the shuttle bus.
    prev_location (dict): Dictionary of previous Airtag locations for each shuttle bus.

Returns:
    list: List of AirTag instances representing unique data points.
"""
class Airtags:
    @staticmethod
    def get_airtags(shuttle_bus, prev_location):
        airtags = []

        prev_address, prev_name = "", ""
        location = None
        if prev_location[shuttle_bus]:
            prev_address = prev_location[shuttle_bus].street_address
            prev_name = prev_location[shuttle_bus].street_name

        with open("./Airtags.csv", encoding="utf-8") as file:
            reader = csv.reader(file, delimiter=",")
            header = next(reader)

            for _, line in enumerate(reader):
                name = line[1]
                if name == shuttle_bus:
                    street_address = line[6]
                    street_name = line[7]
                    if (street_address, street_name) != (prev_address, prev_name):
                        location = AirTag(
                                datetime=line[0],
                                name=line[1],
                                battery_status=line[2],
                                position_type=line[3],
                                latitude=line[4],
                                longitude=line[5],
                                street_address=line[6],
                                street_name=line[7],
                                area_of_interest_a=line[8],
                                area_of_interest_b=line[9]
                            )
                        airtags.append(location)
                    prev_address, prev_name = street_address, street_name
                    if location:
                        prev_location[shuttle_bus] = location
        
        # Erase all data on Airtags.csv 
        # By erasing all data this program will only read the newest entries 
        if shuttle_bus == "CCNY Shuttle 3":
            with open("./Airtags.csv", "w", newline='', encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(header)

        return airtags
