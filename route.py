import requests
import Constants

# To-do
# Add Error handling for post request

class Route:
    def __init__(self):
        self.api_url = "https://routes.googleapis.com/directions/v2:computeRoutes"
        self.api_key = Constants.MAP_API_KEY
        self.headers = {"Content-Type": "application/json", 
                        "X-Goog-Api-Key":self.api_key,
                        "X-Goog-FieldMask":"routes.duration,routes.distanceMeters,routes.polyline.encodedPolyline"}

    def fetch_route(self, origin_latitude, origin_longitude, destination_latitude, destination_longitude, intermediates_latitude=None, intermediates_longitude=None):
        route_request = {"origin": {
                            "location":{
                                "latLng":{
                                    "latitude": origin_latitude,
                                    "longitude": origin_longitude,
                                    }
                                }
                            },
                         "destination": {
                                "location":{
                                    "latLng":{
                                        "latitude": destination_latitude,
                                        "longitude": destination_longitude
                                        }
                                }
                            },
                         "travelMode": "DRIVE",
                         "routingPreference": "TRAFFIC_AWARE",
                         "languageCode": "en_US",
                         "units": "IMPERIAL",
                }
       
        if intermediates_latitude and intermediates_longitude:
            waypoint = {
                "location": {
                    "latLng": {
                        "latitude": intermediates_latitude,
                        "longitude": intermediates_longitude
                    }
                }
            }
            route_request["intermediates"] = waypoint
          
        response = requests.post(self.api_url,headers=self.headers, json=route_request)  
        return response.json()


#fetchRoute = Route()

#response_data = fetchRoute.getRoute(40.820043999999996, -73.949822100000006, 40.82377614314247, -73.94502568555461)
#print(response_data)




