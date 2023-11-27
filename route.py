import requests
import Constants

class Route:
    def __init__(self):
        # Initialize the Route class with Google Map Route API and API key
        self.api_url = "https://routes.googleapis.com/directions/v2:computeRoutes"
        self.api_key = Constants.MAP_API_KEY

        # Define header for api request
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

        # If intermediate points are provided, include them in the request
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


# For Testing Purpose
# To test run 'python route.py' in terminal
if __name__== '__main__':
    fetchRoute = Route()

    response_data = fetchRoute.fetch_route(40.819557163853155, -73.94991793531442, 40.82377614314247, -73.94502568555461)
    print(response_data)




