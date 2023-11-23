from bus_stop import BusStop
from route import Route
from geocoding import Geocoding

# To-do
# Make this code more modular
# Error handling needs to be added
# Create Enum for All Street Names

# All Bus Stops and Intermediates shuttle bus will pass 
BUS_STOPS = {
    'W145': BusStop(1, "W145", 40.82377614314247, -73.94502568555461, 691, "St Nicholas Ave"),  # 691 St Nicholas Ave
    'NAC': BusStop(2, "NAC", 40.819557163853155, -73.94991793531442, 201, "Convent Ave"),  # 201 The City College of New York
    'W125': BusStop(3, "W125", 40.8103721597239, -73.95278450679731, 284, "St Nicholas Ave"),  # 284 St Nicholas Ave # W 124th St
    'intermediate_to_125': BusStop(4, "intermediate_125", 40.810976077358795, -73.95405670678701),
    'intermediate_to_nac': BusStop(5, "intermediate_nac", 40.811255, -73.953659),
}

class BusRoute:
    def __init__(self, previous_route, datetime, name, latitude, longitude, street_address, street_name, interest_a):
        # Data from Airtags
        self.datetime = datetime
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.street_address = street_address
        self.street_name = street_name
        self.interest_a = interest_a

        # Data from Google Route API
        self.distance = None
        self.duration = None
        self.polyline = None

        # Determine Bus Direction
        # BusStop datatype
        self.next_stop = None
        self.intermediate = None
        self.previous_stop = None

        # Route datatype
        self.previous_route = previous_route

    # Retrieve Route from route.py using Google MAP API
    def fetch_route(self):
        # Initialize Route API
        bus_route = Route()

        destination_latitude = self.next_stop.latitude
        destination_longitude = self.next_stop.longitude

        if self.intermediate:
            intermediates_latitude = self.intermediate.latitude
            intermediates_longitude = self.intermediate.longitude
            response = bus_route.fetch_route(self.latitude, self.longitude, destination_latitude, destination_longitude, intermediates_latitude, intermediates_longitude)
        else:
            response = bus_route.fetch_route(self.latitude, self.longitude, destination_latitude, destination_longitude)

        # Update distance, duration, polyline
        try:
            self.distance = response['routes'][0]['distanceMeters']
        except (KeyError, IndexError):
            self.distance = None

        try:
            self.duration = response['routes'][0]['duration']
        except (KeyError, IndexError):
            self.duration = None

        try:
            self.polyline = response['routes'][0]['polyline']['encodedPolyline']
        except (KeyError, IndexError):
            self.polyline = None

    # Determine Bus Next Stop
    def get_next_stop(self):
        self.clean_data()
        self.adjust_origin()
        self.get_previous_stop()
        
        # Reached Bus Stops
        if self.reached_w145():
            return
        if self.reached_ccny():
            return
        if self.reached_w125():
            return
        
        # if airtag did not update at the bus stop
        if self.previous_route:
            self.skipped_stop()
            return
    
    def skipped_stop(self):
        if (210 < int(self.street_address) <= 355 and self.street_name == "Convent Ave") and self.previous_route.previous_stop == BUS_STOPS['W125']:
            self.next_stop = BUS_STOPS['W145']
            self.previous_stop = BUS_STOPS['NAC']
            return
        
        if ((135 >= int(self.street_address) and self.street_name == "Convent Ave") or self.street_name == "Morningside Ave" ) and self.previous_route.previous_stop == BUS_STOPS['W145'] :
            self.next_stop = BUS_STOPS['W125']
            self.previous_stop = BUS_STOPS['NAC']
            return
            
    def reached_w145(self):
        if (int(self.street_address) >= 630 and self.street_name == "St Nicholas Ave") or self.street_name == "W 145th St" or self.street_name == "W 141st St" or (self.interest_a == "145 St" and self.street_address == ""): #145
            self.next_stop = BUS_STOPS['NAC']
            self.previous_stop = BUS_STOPS['W145']
            return True
        return False

    def reached_w125(self):
        if (100 <= int(self.street_address) <= 300 and self.street_name == "St Nicholas Ave") or self.street_name == "Hancock Pl" or (self.street_name == "W 125th St" and int(self.street_address) < 400) or self.street_name == "W 124th St" or self.street_name == "Manhattan Ave": #125
            self.next_stop = BUS_STOPS['NAC']
            self.intermediate = BUS_STOPS['intermediate_to_nac']
            self.previous_stop = BUS_STOPS['W125']
            return True
        if int(self.street_address) == 0 and self.street_name == "St Nicholas Ave":
            if self.interest_a == "125 St":
                self.next_stop = BUS_STOPS['NAC']
                self.intermediate = BUS_STOPS['intermediate_to_nac']
                self.previous_stop = BUS_STOPS['W125']
                return True
            else:
                self.next_stop = BUS_STOPS['NAC']
                self.previous_stop = BUS_STOPS['W145']
                return True
        return False

    def reached_ccny(self):
        if ((150 <= int(self.street_address) <= 210)  and self.street_name == "Convent Ave") or (self.interest_a == "The City College of New York" and self.street_address == ""): # CCNY
            if self.previous_stop == BUS_STOPS['W125']: # going to w145
                self.next_stop = BUS_STOPS['W145']
                self.previous_stop = BUS_STOPS['NAC']
                return True
            elif self.previous_stop == BUS_STOPS['W145']: # going to w125
                self.next_stop = BUS_STOPS['W125']
                self.intermediate = BUS_STOPS['intermediate_to_125']
                self.previous_stop = BUS_STOPS['NAC']
                return True
        return False
    
    def get_previous_stop(self):
        if self.previous_route:
            self.previous_stop = self.previous_route.previous_stop
        else:
            self.previous_stop = BUS_STOPS['NAC']

    # If Airtag Location is slightly off the route, Re-adjust the location, This happened due to airtag pinging off from a radius
    def adjust_origin(self):
        if self.street_name == "Hamilton Terr":
            self.latitude = 40.821713 
            self.longitude = -73.947070
            self.street_name = "W 141st St"
            self.street_address = 428
            return
        
        if self.street_name == "Amsterdam Ave" and 1510 <= int(self.street_address) <= 1617:
            self.latitude = 40.8198374
            self.longitude = -73.9505743
            self.street_name = "Convnet Ave"
            self.street_address = 160
            return
        
        # Need to Add Exception
        if self.street_name == "Amsterdam Ave" and 1360 < int(self.street_address) < 1510:
            new_coordinates = Geocoding()
            result = new_coordinates.fetch_coordinates(int(self.street_address) - 1360, "Convnet Ave")

            self.latitude = result['lat']
            self.longitude = result['lng']
            self.street_name = "Convnet Ave"
            self.street_address = int(self.street_address) - 1360
            return
        
        if (self.street_name == "St Nicholas Terr" and int(self.street_address) > 250) or self.street_name == "W 140th St":
            self.latitude = 40.81991080221068
            self.longitude = -73.94967653138818
            self.street_name = "Convent Ave"
            self.street_address = 255
            return

        if (int(self.street_address) >= 630 and self.street_name == "St Nicholas Ave"):
            if int(self.street_address) % 2 == 0:
                new_coordinates = Geocoding()
                result = new_coordinates.fetch_coordinates(int(self.street_address) +1, self.street_name)

                self.latitude = result['lat']
                self.longitude = result['lng']
                self.street_address = int(self.street_address) +1

                return
    # Handlde any NULL values, or String values on streetaddress within the data collected
    def clean_data(self):
        if not self.street_address or self.street_address == ' ':
            self.street_address = 0
        if not self.street_name or self.street_name == ' ':
            self.street_name = ""
        if type(self.street_address) == str and "–" in self.street_address:
            self.street_address = int(self.street_address.split('–')[0])

    # Retreive the Last Location the bus was headed
    def get_last_destination(self):
        if not self.previous_route:
            self.next_stop = BUS_STOPS['NAC']
            return
        self.next_stop = self.previous_route.next_stop
        self.intermediate = self.previous_route.intermediate

    # Clear any Intermediate On the route that is not suppose to be on
    def delete_intermediate(self):
        streets = ["St Nicholas Ave", "Hancock Pl", "W 125th St", "W 124th St"]
        if (int(self.street_address) <= 300 and self.street_name == "St Nicholas Ave") or self.street_name in streets:
            self.intermediate = None

    # Return Json Format of this object
    def to_json(self):
        return {
            "datetime":self.datetime,
            "name":self.name,
            "latitude" :self.latitude,
            "longitude" :self.longitude,
            "street_address" : self.street_address,
            "street_name" : self.street_name,
            "distance" : self.distance,
            "duration" : self.duration,
            "prev_stop": self.previous_stop.name,
            "next_stop" : self.next_stop.name,
            "polyline" : self.polyline
        }
    