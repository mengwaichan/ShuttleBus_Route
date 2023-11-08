from getairtag import Airtags
from busRoutes import BusRoutes
import csv

def processShuttleBus(name, prevShuttle):
    locations = Airtags.get_airtag(name)
    output_file = f"{name.replace(' ', '_')}_route_data.csv"

    with open(output_file, 'w', newline='') as csv_file:
        # Define the CSV writer
        writer = csv.writer(csv_file)

        # Write the header row to the CSV
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
            prev = prevShuttle[name]
            route = BusRoutes(
                locations[i].dateTime.strip(), 
                locations[i].name.strip(), 
                float(locations[i].locationLatitude.strip()),
                float(locations[i].locationLongitude.strip()),
                locations[i].addressStreetAddress.strip(),
                locations[i].addressStreetName.strip()
            )
        
            route.getLastDest(prev)
            route.get_nextStop(prev)
            route.fetchRoute()
            route.deleteIntermediate()

            prev_shuttle[name] = route
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

prev_shuttle = {"CCNY Shuttle 1": None, "CCNY Shuttle 2": None, "CCNY Shuttle 3": None, }
shuttleBuses = ["CCNY Shuttle 1", "CCNY Shuttle 2", "CCNY Shuttle 3"]
for shuttleBus in shuttleBuses:
    processShuttleBus(shuttleBus, prev_shuttle)
