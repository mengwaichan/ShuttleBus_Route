import csv
import time
from airtags import Airtags
from bus_route import BusRoute
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

"""
CCNY Shuttle Tracking Script

This script processes location data from Airtags and generates bus routes for CCNY Shuttles.
It writes the route and location data to CSV files and stores them in Firestore.
The script runs continuously, reading new data every minute.

Usage:
- Ensure the required Python packages are installed (Firebase).
- Set up Firestore credentials in 'Firebase_auth.json'.
- Run the script to start tracking CCNY Shuttles.

# TODO
# Use Flask to build an API to add, delete, or restrict bus stops
"""

SLEEP_TIME = 60
ROUTE_OUTPUT_FILE_SUFFIX = "_route_data.csv"
LOCATION_OUTPUT_FILE_SUFFIX = "_location_data.csv"

def initialize_firestore():
    """
    Initialize the Firestore client using credentials from 'Firebase_auth.json'.

    Returns:
        google.cloud.firestore.Client: Firestore client instance.
    """
    cred = credentials.Certificate('./Firebase_auth.json')
    firebase_admin.initialize_app(cred)
    return firestore.client()

def add_data_to_firestore(collection_name, data):
    """
    Add data to Firestore.

    Args:
        collection_name (str): Name of the Firestore collection.
        data (dict): Data to be added to the collection.

    Returns:
        None
    """
    db.collection(collection_name).add(data)

def write_route_data(writer, route):
    """
    Write route data to a CSV file and Firestore.

    Args:
        writer: CSV writer object.
        route (BusRoute): BusRoute instance containing route information.

    Returns:
        None
    """
    previous_stop = ""
    if route.previous_stop:
        previous_stop = route.previous_stop.name

    writer.writerow(
        [route.datetime, 
        route.name,
        route.arrival_time, 
        route.latitude, 
        route.longitude, 
        route.street_address, 
        route.street_name, 
        route.distance,
        route.duration,
        previous_stop,
        route.next_stop.name,
        route.delta,
        route.polyline])

    # Data to be written to Firestore
    firestore_route_data = {
        'datetime': route.datetime,
        'name': route.name,
        'arrivaltime': route.arrival_time,
        'latitude': route.latitude,
        'longitude': route.longitude,
        'streetaddress': route.street_address,
        'streetname': route.street_name,
        'distance': route.distance,
        'duration': route.duration,
        'prevStop': previous_stop,
        'nextStop': route.next_stop.name,
        'delta': route.delta,
        'duration_delta': route.duration_delta,
        'polyline': route.polyline
    }

    # Write Route data to Firestore
    collection_name_route = "CCNY_Shuttle_Routing"
    add_data_to_firestore(collection_name_route, firestore_route_data)

def write_location_data(writer, location, name):
    """
    Write location data to a CSV file and Firestore.

    Args:
        writer: CSV writer object.
        location (AirtagsLocation): Airtags Location instance containing location information.
        name (str): Name of the shuttle bus.

    Returns:
        None
    """
    #
    writer.writerow(
        [location.datetime.strip(), 
        location.name.strip(), 
        int(location.battery_status.strip()),
        location.position_type.strip(),
        float(location.latitude.strip()),
        float(location.longitude.strip()),
        location.street_address.strip(),
        location.street_name.strip(),
        location.area_of_interest_a.strip(),
        location.area_of_interest_b.strip()              
        ])
    
    # Data to be written to Firestore
    firestore_location_data = {
        'datetime' : location.datetime.strip(), 
        'name' : location.name.strip(), 
        'locationlatitude' : float(location.latitude.strip()),
        'locationlongitude' : float(location.longitude.strip()),
        'addressstreetaddress': location.street_address.strip(),
        'addressstreetname' : location.street_name.strip(),
        'addressareaofinteresta': location.area_of_interest_a.strip(),
        'addressareaofinterestb': location.area_of_interest_b.strip(),
        'batterystatus' : int(location.battery_status.strip()),
        'locationpositiontype' : location.position_type.strip()
    }

    # Write location data to Firestore
    collection_name_locations = name.replace(' ', '_')
    add_data_to_firestore(collection_name_locations, firestore_location_data)

def create_bus_route(prev_route, location):
    """
    Create a BusRoute instance from previous route data and a new location.

    Args:
        prev_route (BusRoute): Previous BusRoute instance.
        location (AirtagsLocation): Airtags Location instance containing location information.

    Returns:
        BusRoute: Newly created BusRoute instance.
    """
    route = BusRoute(
        prev_route,
        location.datetime.strip(), 
        location.name.strip(), 
        float(location.latitude.strip()),
        float(location.longitude.strip()),
        location.street_address.strip(),
        location.street_name.strip(),
        location.area_of_interest_a.strip()
    )

    route.get_time_difference()
    route.get_next_stop()
    route.fetch_route()
    route.delete_intermediate()
    # route.calculate_delta()
    route.not_in_range()
    route.get_arrival_time()

    return route
    
def process_shuttle_bus(name, prev_route, prev_location):
    """
    Process Airtags data, generate routes, and write to CSV and Firestore.

    Args:
        name (str): Name of the shuttle bus.
        prev_route (dict): Dictionary of previous BusRoute instances for each shuttle bus.
        prev_location (dict): Dictionary of previous Airtags Location instances for each shuttle bus.

    Returns:
        None
    """
    # Retieve location Data from Airtags.csv
    locations = Airtags.get_airtags(name, prev_location)

    # Create route.csv and location.csv to store 
    output_file_route = f"{name.replace(' ', '_')}{ROUTE_OUTPUT_FILE_SUFFIX}"
    output_file_location = f"{name.replace(' ', '_')}{LOCATION_OUTPUT_FILE_SUFFIX}"

    with open(output_file_route, 'a', newline='') as csv_file_route, open(output_file_location, 'a', newline='') as csv_file_location:
        writer_route = csv.writer(csv_file_route)
        writer_location = csv.writer(csv_file_location)

        # Write header row to the CSVs
        if csv_file_route.tell() == 0:
            writer_route.writerow(
                ['datetime', 
                'name', 
                'arrivaltime',
                'latitude', 
                'longitude', 
                'streetaddress', 
                'streetname', 
                'distance', 
                'duration',
                'prevStop',
                'nextStop',
                'delta',
                'polyline'])  

        if csv_file_location.tell() == 0:
                writer_location.writerow(
                    ['datetime',
                     'name',
                     'locationlatitude',
                     'locationlongitude',
                     'addressstreetaddress',
                     'addressstreetname',
                     'addressareaofinteresta',
                     'addressareaofinterestb',
                     'batterystatus',
                     'locationpositiontype'])
        
        # Create bus route and writing to csv and firebase for every location in Airtags.csv
        for i in range(len(locations)):
            route = create_bus_route(prev_route[name], locations[i])

            prev_route[name] = route
                
            write_route_data(writer_route, route)
            write_location_data(writer_location, locations[i], name)
            

# HashMap to track last location read from Airtags.csv and last route generated by Google API
prev_route = {"CCNY Shuttle 1": None, "CCNY Shuttle 2": None, "CCNY Shuttle 3": None }
shuttle_buses = ["CCNY Shuttle 1", "CCNY Shuttle 2", "CCNY Shuttle 3"]
prev_location = {"CCNY Shuttle 1": None, "CCNY Shuttle 2": None, "CCNY Shuttle 3": None }

# Initialize Firestore instance
db = initialize_firestore()

while True:
    for shuttleBus in shuttle_buses:
        process_shuttle_bus(shuttleBus, prev_route, prev_location)
    
    time.sleep(SLEEP_TIME)
