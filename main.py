import csv
import time
from airtags import Airtags
from bus_route import BusRoute
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# To-do
# Break process_shuttle_bus() into smaller pieces
# Add Error Handling
#
# Use Flask to build an API to add, delete, or restrict bus stops

SLEEP_TIME = 60
OUTPUT_FILE_SUFFIX = "_route_data.csv"

cred = credentials.Certificate('./Firebase_auth.json')
firebase_admin.initialize_app(cred)

# Initialize Firestore instance
db = firestore.client()

# Function to add data to Firestore
def add_data_to_firestore(collection_name, data):
    db.collection(collection_name).add(data)


def process_shuttle_bus(name, prev_route, prev_location):
    # Retieve location Data from Airtags.csv
    locations = Airtags.get_airtags(name, prev_location)

    output_file = f"{name.replace(' ', '_')}{OUTPUT_FILE_SUFFIX}"

    with open(output_file, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)

        # Write the header row to the CSV
        if csv_file.tell() == 0:
            writer.writerow(
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

        for i in range(len(locations)):
            prev = prev_route[name]
            route = BusRoute(
                prev,
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
            writer.writerow(
                [route.datetime, 
                route.name, 
                route.latitude, 
                route.longitude, 
                route.street_address, 
                route.street_name, 
                route.distance,
                route.duration,
                prev_stop,
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
                'prevStop': prev_stop,
                'nextStop': route.next_stop.name,
                'polyline': route.polyline
            }

            # Write data to Firestore
            collection_name_route = "CCNY_Shuttle_Routing"
            add_data_to_firestore(collection_name_route, firestore_route_data)

            firestore_location_data = {
                'datetime' : locations[i].datetime.strip(), 
                'name' : locations[i].name.strip(), 
                'locationlatitude' : float(locations[i].latitude.strip()),
                'locationlongitude' : float(locations[i].longitude.strip()),
                'addressstreetaddress': locations[i].street_address.strip(),
                'addressstreetname' : locations[i].street_name.strip(),
                'addressareaofinteresta': locations[i].area_of_interest_a.strip(),
                'addressareaofinterestb': locations[i].area_of_interest_b.strip(),
                'batterystatus' : int(locations[i].battery_status.strip()),
                'locationpositiontype' : locations[i].position_type.strip()
            }
            
            collection_name_locations = name.replace(' ', '_')
            add_data_to_firestore(collection_name_locations, firestore_location_data)

# HashMap to track last location and last route
prev_route = {"CCNY Shuttle 1": None, "CCNY Shuttle 2": None, "CCNY Shuttle 3": None }
shuttle_buses = ["CCNY Shuttle 1", "CCNY Shuttle 2", "CCNY Shuttle 3"]
prev_location = {"CCNY Shuttle 1": None, "CCNY Shuttle 2": None, "CCNY Shuttle 3": None }

while True:
    for shuttleBus in shuttle_buses:
        process_shuttle_bus(shuttleBus, prev_route, prev_location)
    
    time.sleep(SLEEP_TIME)
