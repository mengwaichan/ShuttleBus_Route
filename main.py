import csv
import time
from airtags import Airtags
from bus_route import BusRoute
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# TODO
# Break process_shuttle_bus() into smaller pieces
# Add Error Handling
#
# Use Flask to build an API to add, delete, or restrict bus stops

SLEEP_TIME = 60
ROUTE_OUTPUT_FILE_SUFFIX = "_route_data.csv"
LOCATION_OUTPUT_FILE_SUFFIX = "_location_data.csv"

# Function to add data to Firestore
def add_data_to_firestore(collection_name, data):
    db.collection(collection_name).add(data)

# Write data to CSV and Firebase
def write_route_data(writer, route, previous_stop):
    writer.writerow(
        [route.datetime, 
        route.name, 
        route.latitude, 
        route.longitude, 
        route.street_address, 
        route.street_name, 
        route.distance,
        route.duration,
        previous_stop,
        route.next_stop.name,
        route.polyline])

    # Data to be written to Firestore
    firestore_route_data = {
        'datetime': route.datetime,
        'name': route.name,
        'latitude': route.latitude,
        'longitude': route.longitude,
        'streetaddress': route.street_address,
        'streetname': route.street_name,
        'distance': route.distance,
        'duration': route.duration,
        'prevStop': previous_stop,
        'nextStop': route.next_stop.name,
        'polyline': route.polyline
    }

    # Write Route data to Firestore
    collection_name_route = "CCNY_Shuttle_Routing"
 #   add_data_to_firestore(collection_name_route, firestore_route_data)

def write_location_data(writer, location, name):
    # Write Location data to csv and firebase
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
#    add_data_to_firestore(collection_name_locations, firestore_location_data)

def process_shuttle_bus(name, prev_route, prev_location):
    # Retieve location Data from Airtags.csv
    locations = Airtags.get_airtags(name, prev_location)

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
                'latitude', 
                'longitude', 
                'streetaddress', 
                'streetname', 
                'distance', 
                'duration',
                'prevStop',
                'nextStop',
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
        
        for i in range(len(locations)):
            route = BusRoute(
                prev_route[name],
                locations[i].datetime.strip(), 
                locations[i].name.strip(), 
                float(locations[i].latitude.strip()),
                float(locations[i].longitude.strip()),
                locations[i].street_address.strip(),
                locations[i].street_name.strip(),
                locations[i].area_of_interest_a.strip()
            )

            route.get_last_destination()
            route.get_next_stop()
            route.fetch_route()
            route.delete_intermediate()

            prev_route[name] = route
            prev_stop = route.previous_stop
            if not prev_stop:
                prev_stop = ""
            else:
                prev_stop = route.previous_stop.name

            write_route_data(writer_route, route, prev_stop)

            write_location_data(writer_location, locations[i], name)
            

# HashMap to track last location and last route
prev_route = {"CCNY Shuttle 1": None, "CCNY Shuttle 2": None, "CCNY Shuttle 3": None }
shuttle_buses = ["CCNY Shuttle 1", "CCNY Shuttle 2", "CCNY Shuttle 3"]
prev_location = {"CCNY Shuttle 1": None, "CCNY Shuttle 2": None, "CCNY Shuttle 3": None }

cred = credentials.Certificate('./Firebase_auth.json')
firebase_admin.initialize_app(cred)

# Initialize Firestore instance
db = firestore.client()

while True:
    for shuttleBus in shuttle_buses:
        process_shuttle_bus(shuttleBus, prev_route, prev_location)
    
    time.sleep(SLEEP_TIME)
