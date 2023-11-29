from bus_stop import BusStop
from route import Route
from geocoding import Geocoding
#from predicted_delta import Predict_Delta
from datetime import datetime, timedelta

# TODO
# Error handling needs to be added
# Create Enum for All Street Names

# All Bus Stops and Intermediates shuttle bus will pass 
BUS_STOPS = {
    'W145': BusStop(1, "W145", 40.82377614314247, -73.94502568555461, 691, "St Nicholas Ave"),  # 691 St Nicholas Ave
    'NAC': BusStop(2, "NAC", 40.819557163853155, -73.94991793531442, 201, "Convent Ave"),  # 201 The City College of New York
    'W125': BusStop(3, "W125", 40.8103721597239, -73.95278450679731, 284, "St Nicholas Ave"),  # 284 St Nicholas Ave # W 124th St
    'intermediate_to_125': BusStop(4, "intermediate_125", 40.810976077358795, -73.95405670678701),
    'intermediate_to_nac': BusStop(5, "intermediate_nac", 40.811255, -73.953659),
    'intermediate_145_nac': BusStop(6, "intermediate_145_nac", 40.821397, -73.946092)
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
        
        # Using arrival_time to sync across all devices when pull from firebase
        # Use arrival_time - current_time to get the duration + delta
        self.arrival_time = None
        # Data from Google Route API
        self.distance = None
        self.duration = None
        self.polyline = None
        self.delta = 0
        self.duration_delta = 0

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

        # Fetch route with Google Route API
        if self.intermediate:
            intermediates_latitude = self.intermediate.latitude
            intermediates_longitude = self.intermediate.longitude
            response = bus_route.fetch_route(
                self.latitude, self.longitude, destination_latitude, destination_longitude, intermediates_latitude, intermediates_longitude)
        else:
            response = bus_route.fetch_route(
                self.latitude, self.longitude, destination_latitude, destination_longitude)

        # Update distance, duration, polyline
        try:
            self.distance = response['routes'][0]['distanceMeters']
        except (KeyError, IndexError):
            self.distance = 0

        try:
            self.duration = response['routes'][0]['duration']
        except (KeyError, IndexError):
            self.duration = 0

        try:
            self.polyline = response['routes'][0]['polyline']['encodedPolyline']
        except (KeyError, IndexError):
            self.polyline = ""

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
    
    # Handle Cases Based on where the bus is
    def skipped_stop(self):
        is_w145_route = (((249 < int(self.street_address) <= 360 and self.street_name == "Convent Ave") or 
                          self.street_name in ["W 140th St", "W 141st St", "W 142nd St", "W 143rd St", "W 144th St"])
                        )

        is_w125_route = (((135 >= int(self.street_address) and self.street_name == "Convent Ave") or self.street_name == "Morningside Ave" or 
                         self.street_name in ["W 135th St", "W 133rd St", "W 131st St", "W 130th St", "W 129th St", "W 128th St", "W 127th St", "W 126th St"]) 
                        )

        if is_w145_route and self.previous_route.previous_stop == BUS_STOPS['W125']:
            self.next_stop = BUS_STOPS['W145']
            self.previous_stop = BUS_STOPS['NAC']
            return
        
        if is_w125_route:
            if self.previous_route.previous_stop == BUS_STOPS['W145']:
                self.next_stop = BUS_STOPS['W125']
                self.previous_stop = BUS_STOPS['NAC']
                return
            elif self.previous_route.next_stop == BUS_STOPS['W145']:
                self.next_stop = BUS_STOPS['W125']
                self.previous_stop = BUS_STOPS['NAC']
                return
    
    def reached_w145(self):
        is_w145 = ((int(self.street_address) >= 630 and self.street_name == "St Nicholas Ave") or 
                   (self.interest_a == "145 St" and self.street_address == "") or
                   self.street_name in ["W 145th St", "W 141st St"])

        if is_w145:
            if self.street_name == "W 145th St":
                self.next_stop = BUS_STOPS['NAC']
                self.previous_stop = BUS_STOPS['W145']
                self.intermediate = BUS_STOPS['intermediate_145_nac']
                self.delta = 180
                return True
            else: 
                self.next_stop = BUS_STOPS['NAC']
                self.previous_stop = BUS_STOPS['W145']
                self.intermediate = None
                self.delta = 60
                return True
        return False

    def reached_w125(self):
        is_w125 = ((100 <= int(self.street_address) <= 300 and self.street_name == "St Nicholas Ave") or 
                   self.street_name in ["Hancock Pl", "W 124th St", "Manhattan Ave", "W 125th St"] or 
                   self.interest_a == "Hancock Park")
        
        if is_w125:
            self.next_stop = BUS_STOPS['NAC']
            self.intermediate = BUS_STOPS['intermediate_to_nac']
            self.previous_stop = BUS_STOPS['W125']
            self.delta = 60
            return True
        
        # Special Case
        if int(self.street_address) == 0 and self.street_name == "St Nicholas Ave":
            if self.interest_a == "125 St":
                self.next_stop = BUS_STOPS['NAC']
                self.intermediate = BUS_STOPS['intermediate_to_nac']
                self.previous_stop = BUS_STOPS['W125']
                self.delta = 60
                return True
            else:
                self.next_stop = BUS_STOPS['NAC']
                self.previous_stop = BUS_STOPS['W145']
                self.intermediate = None
                self.delta = 180
                return True
        return False

    def reached_ccny(self):
        is_ccny = (((150 <= int(self.street_address) <= 210)  and self.street_name == "Convent Ave") or 
                   (self.interest_a == "The City College of New York" and self.street_address == ""))
       
        if is_ccny: # CCNY
            if self.previous_stop == BUS_STOPS['W125']: # going to w145
                self.next_stop = BUS_STOPS['W145']
                self.previous_stop = BUS_STOPS['NAC']
                self.intermediate = None
                self.delta = 240
                return True
            elif self.previous_stop == BUS_STOPS['W145']: # going to w125
                self.next_stop = BUS_STOPS['W125']
                self.intermediate = BUS_STOPS['intermediate_to_125']
                self.previous_stop = BUS_STOPS['NAC']
                self.delta = 240
                return True
        return False
    
    # Get Previous Stop based on Previous Route
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

        # Add CCNY Cases
        if(int(self.street_address) == 160 or int(self.street_address) == 200 )and self.street_name == "Convent Ave" :
            self.latitude = 40.819557163853155
            self.longitude = -73.94991793531442
        if int(self.street_address) == 150 and self.street_name == "Convent Ave" :
            self.latitude = 40.8183630579255 
            self.longitude = -73.95096568242835
        
        if int(self.street_address) == 164 and self.street_name == "Convent Ave":
            self.latitude = 40.81874083074161
            self.longitude = -73.95056421534208

        if int(self.street_address) == 240 and self.street_name == "Convent Ave":
            self.latitude = 40.821213376345355
            self.longitude = -73.94877793264239
    
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

    # Calculate Delta for more accurarte 
    # def calculate_delta(self):
    #     delta = Predict_Delta(self.distance, self.previous_stop.name, self.next_stop.name)
    #     self.delta = delta

    # Calculate Arrival Time datetime + duration + delta
    def get_arrival_time(self):
        airtag_timestamp = datetime.strptime(self.datetime, '%Y-%m-%d %H:%M:%S')

        new_datetime = airtag_timestamp + timedelta(seconds = (int(self.duration.rstrip('s')) + self.delta))

        self.arrival_time = new_datetime.strftime('%Y-%m-%d %H:%M:%S')

        self.duration_delta = (int(self.duration.rstrip('s')) + self.delta)

    def overtime(self):
        current_datetime = datetime.strptime(self.datetime, "%Y-%m-%d %H:%M:%S")
        if self.previous_route:
            previous_datetime = datetime.strptime(self.previous_route.datetime, "%Y-%m-%d %H:%M:%S")
        else:
            previous_datetime = current_datetime
        time_difference = (current_datetime - previous_datetime).total_seconds()

        if time_difference > 900:
            self.polyline = ""
            self.duration = "0s"
            self.distance = 0

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
            "polyline" : self.polyline,
            "arrival_time": self.arrival_time,
            "delta": self.delta
        }
    