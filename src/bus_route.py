from src.bus_stop import BusStop
from src.route import Route
from src.geocoding import Geocoding
# from predict_delta import Predict_Delta
from datetime import datetime, timedelta
from src.stop_predictor import StopPredictor

"""
A class to represent a bus route with information from Airtags and Google Maps API.

Attributes:
    previous_route (BusRoute): The previous route object for prediction.
    datetime (str): The timestamp of the Airtag data.
    name (str): The name of the bus.
    latitude (float): The latitude coordinate of the bus.
    longitude (float): The longitude coordinate of the bus.
    street_address (str): The street address of the bus location.
    street_name (str): The name of the street where the bus is located.
    interest_a (str): Area of interest for route prediction.
    arrival_time (str): The calculated arrival time at the next bus stop.
    distance (int): The distance of the route.
    duration (str): The estimated duration of the route.
    polyline (str): The polyline representation of the route.
    delta (int): The calculated delta for more accurate predictions.
    duration_delta (int): The duration with added delta.
    next_stop (BusStop): The next busstop object.
    previous_stop (BusStop): The previous busstop object.
    
Methods:
    fetch_route: Fetches the route information from the Google Maps API.
    get_next_stop: Determines the next bus stop using a StopPredictor.
    adjust_origin: Adjusts the bus location based on certain conditions.
    clean_data: Handles cleaning and validation of data.
    delete_intermediate: Clears any intermediate stops that are not supposed to be on the route.
    get_arrival_time: Calculates the arrival time based on duration and delta.
    get_time_difference: Calculates the time difference between current and previous Airtag timestamps.
    not_in_range: Clear all polylines and duration if the bus is not range
    to_json: Returns a JSON representation of the BusRoute object.
"""

# TODO
# Include Machine Learning Model for better prediction, remove self.delta in get_next_stop() when implemented 

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
        self.next_stop = None
        self.intermediate = None
        self.previous_stop = None
        self.time_difference = 0

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
            self.duration = "0s"

        try:
            self.polyline = response['routes'][0]['polyline']['encodedPolyline']
        except (KeyError, IndexError):
            self.polyline = ""

    # Determine Bus Next Stop
    def get_next_stop(self):
        self.clean_data()
        self.adjust_origin()
        
        # StopPredictor to find the next stop for the bus
        bus_stop = StopPredictor(self.street_name, self.street_address, self.interest_a, self.time_difference, self.previous_route)
        bus_stop.get_last_destination()
        bus_stop.get_next_stop()

        self.next_stop = bus_stop.next_stop
        self.previous_stop = bus_stop.previous_stop
        self.intermediate = bus_stop.intermediate
        self.delta = bus_stop.delta
        
    # If Airtag Location is slightly off the route, Re-adjust the location, This happened due to airtag pinging off from a radius
    def adjust_origin(self):
        # Adjust lat, lng to W 141 St
        if self.street_name == "Hamilton Terr":
            self.latitude = 40.821713 
            self.longitude = -73.947070
            self.street_name = "W 141st St"
            self.street_address = 428
            return
        
        # Adjust lat, lng from Amsterdam Ave to Convent Ave
        if self.street_name == "Amsterdam Ave" and 1510 <= int(self.street_address) <= 1617:
            self.latitude = 40.8198374
            self.longitude = -73.9505743
            self.street_name = "Convnet Ave"
            self.street_address = 160
            return
        
        if self.street_name == "Amsterdam Ave" and 1360 < int(self.street_address) < 1510:
            new_coordinates = Geocoding()
            result = new_coordinates.fetch_coordinates(int(self.street_address) - 1360, "Convnet Ave")

            self.latitude = result['lat']
            self.longitude = result['lng']
            self.street_name = "Convnet Ave"
            self.street_address = int(self.street_address) - 1360
            return
        
        # Adjust lat, lng to Convent Ave
        if (self.street_name == "St Nicholas Terr" and int(self.street_address) > 250) or self.street_name == "W 140th St":
            self.latitude = 40.81991080221068
            self.longitude = -73.94967653138818
            self.street_name = "Convent Ave"
            self.street_address = 255
            return

        # Adjust lat, lng to the other side of the road near W 145 St Station
        if (int(self.street_address) >= 630 and self.street_name == "St Nicholas Ave"):
            if int(self.street_address) % 2 == 0:
                new_coordinates = Geocoding()
                result = new_coordinates.fetch_coordinates(int(self.street_address) +1, self.street_name)

                self.latitude = result['lat']
                self.longitude = result['lng']
                self.street_address = int(self.street_address) +1
                return

        # CCNY Special Cases
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

    # Clear any Intermediate On the route that is not suppose to be on
    def delete_intermediate(self):
        streets = ["St Nicholas Ave", "Hancock Pl", "W 125th St", "W 124th St"]
        if (int(self.street_address) <= 300 and self.street_name == "St Nicholas Ave") or self.street_name in streets:
            self.intermediate = None

        if(self.next_stop.name == "W145"):
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

    # Calculate the difference between current Airtag timestamp from last Airtag timestamp
    def get_time_difference(self):
        current_datetime = datetime.strptime(self.datetime, "%Y-%m-%d %H:%M:%S")
        if self.previous_route:
            previous_datetime = datetime.strptime(self.previous_route.datetime, "%Y-%m-%d %H:%M:%S")
        else:
            previous_datetime = current_datetime
        self.time_difference = (current_datetime - previous_datetime).total_seconds()

    def not_in_range(self):
        if self.distance > 1700:
            self.polyline = ""
            self.duration = "0s"
            self.delta = 0

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
    