"""
A class to represent information about a bus stop.

Attributes:
    stop_id (int): The unique identifier for the bus stop.
    name (str): The name of the bus stop.
    latitude (float): The latitude coordinate of the bus stop.
    longitude (float): The longitude coordinate of the bus stop.
    street_name (str): The name of the street where the bus stop is located (optional).
    street_address (str): The street address of the bus stop (optional).

Example:
    stop = BusStop(stop_id=1, name="Main Street", latitude=40.123, longitude=-73.456, street_name="Main St", street_address="123 Main St")
"""

class BusStop:
    def __init__(self, stop_id, name, latitude, longitude, street_name = None, street_address = None):
        self.stop_id = stop_id
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.street_name = street_name
        self.street_address = street_address
    
