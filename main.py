from getairtag import Airtags
from busRoutes import BusRoutes
import csv
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# To-do
# Break processShuttleBus() into smaller pieces
# Use Constants instead of hardcoding sleep() and csv name
# Add Error Handling

# Initialize Firebase
cred = credentials.Certificate('./Firebase_auth.json')
firebase_admin.initialize_app(cred)

# Initialize Firestore instance
db = firestore.client()

# Function to add data to Firestore
def add_data_to_firestore(collection_name, data):
    db.collection(collection_name).add(data)


def processShuttleBus(name, prev_route, prev_location):
    # Retieve location Data from Airtags.csv
    locations = Airtags.getAirtag(name, prev_location)

    output_file = f"{name.replace(' ', '_')}_route_data.csv"

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
            route = BusRoutes(
                locations[i].dateTime.strip(), 
                locations[i].name.strip(), 
                float(locations[i].locationLatitude.strip()),
                float(locations[i].locationLongitude.strip()),
                locations[i].addressStreetAddress.strip(),
                locations[i].addressStreetName.strip(),
                locations[i].addressAreaOfInterestA.strip()
            )

            route.setPrev(prev)
            route.getLastDest()
            route.getNextStop()
            route.fetchRoute()
            route.deleteIntermediate()

            prev_route[name] = route
            prevStop = route.prevStop
            if not prevStop:
                prevStop = ""
            else:
                prevStop = route.prevStop.stopName
            writer.writerow(
                [route.datetime, 
                route.name, 
                route.lat, 
                route.lng, 
                route.streetaddress, 
                route.streetname, 
                route.distance,
                route.duration,
                prevStop,
                route.nextStop.stopName,
                route.polyline])

            # Data to be written to Firestore
            firestore_data = {
                'datetime': route.datetime,
                'name': route.name,
                'latitude': route.lat,
                'longitude': route.lng,
                'streetaddress': route.streetaddress,
                'streetname': route.streetname,
                'distance': route.distance,
                'duration': route.duration,
                'prevStop': prevStop,
                'nextStop': route.nextStop.stopName,
                'polyline': route.polyline
            }

            # Write data to Firestore
            collection_name = "CCNY_Shuttle_Routing"
            add_data_to_firestore(collection_name, firestore_data)

# HashMap to track last location and last route
prevRoute = {"CCNY Shuttle 1": None, "CCNY Shuttle 2": None, "CCNY Shuttle 3": None }
shuttleBuses = ["CCNY Shuttle 1", "CCNY Shuttle 2", "CCNY Shuttle 3"]
prevLocation = {"CCNY Shuttle 1": None, "CCNY Shuttle 2": None, "CCNY Shuttle 3": None }

while True:
    for shuttleBus in shuttleBuses:
        processShuttleBus(shuttleBus, prevRoute, prevLocation)
    
    time.sleep(60)
