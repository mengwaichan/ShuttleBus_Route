from getairtag import Airtags
from busRoutes import BusRoutes
import csv

locations = Airtags.get_airtag()
output_file = "route_data.csv"

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
    
    prev = None
    for i in range(len(locations)):
        route = BusRoutes(
            locations[i].dateTime, 
            locations[i].name, 
            locations[i].locationLatitude,
            locations[i].locationLongitude,
            locations[i].addressStreetAddress,
            locations[i].addressStreetName
        )
        
        route.getLastDest(prev)
        route.get_nextStop(prev)
        route.fetchRoute()
        route.deleteIntermediate()

        prev = route
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
