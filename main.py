from getairtag import Airtags
from busRoutes import BusRoutes
import csv
import time

def processShuttleBus(name, prev_route, prev_location):
    locations = Airtags.get_airtag(name, prev_location)

    output_file = f"{name.replace(' ', '_')}_route_data.csv"

    with open(output_file, 'a', newline='') as csv_file:
        # Define the CSV writer
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
        
            route.getLastDest(prev)
            route.get_nextStop(prev)
            route.fetchRoute()
            route.deleteIntermediate()

            prev_route[name] = route
            writer.writerow(
                [route.datetime, 
                route.name, 
                route.lat, 
                route.lng, 
                route.streetaddress, 
                route.streetname, 
                route.distance,
                route.duration,
                route.nextStop.getName(),
                route.polyline])

prev_route = {"CCNY Shuttle 1": None, "CCNY Shuttle 2": None, "CCNY Shuttle 3": None }
shuttleBuses = ["CCNY Shuttle 1", "CCNY Shuttle 2", "CCNY Shuttle 3"]
prev_location = {"CCNY Shuttle 1": None, "CCNY Shuttle 2": None, "CCNY Shuttle 3": None }

while True:
    for shuttleBus in shuttleBuses:
        processShuttleBus(shuttleBus, prev_route, prev_location)
    
    time.sleep(60)
