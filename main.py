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
         'serialnumber', 
         'latitude', 
         'longitude', 
         'streetaddress', 
         'streetname', 
         'distance', 
         'duration',
         'destlatitude',
         'destlongitude'])  

    route = BusRoutes(
            locations[0].dateTime, 
            locations[0].name, 
            locations[0].serialNumber,
            locations[0].locationLatitude,
            locations[0].locationLongitude,
            locations[0].addressStreetAddress,
            locations[0].addressStreetName
        )
    route.get_nextStop()
    route.fetchRoute()

    writer.writerow(
            [route.datetime, 
             route.name, 
             route.serialnumber, 
             route.lat, 
             route.lng, 
             route.streetaddress, 
             route.streetname, 
             route.distance,
             route.duration,
             route.destlat,
             route.destlng])
    
    prev = route

    for i in range(1,len(locations)):
        route = BusRoutes(
            locations[i].dateTime, 
            locations[i].name, 
            locations[i].serialNumber,
            locations[i].locationLatitude,
            locations[i].locationLongitude,
            locations[i].addressStreetAddress,
            locations[i].addressStreetName
        )
        
        route.setdest(prev.destlat, prev.destlng, prev.interlat, prev.interlng)
        route.get_nextStop()
        route.fetchRoute()

        prev = route
        writer.writerow(
            [route.datetime, 
             route.name, 
             route.serialnumber, 
             route.lat, 
             route.lng, 
             route.streetaddress, 
             route.streetname, 
             route.distance,
             route.duration,
             route.destlat,
             route.destlng])
