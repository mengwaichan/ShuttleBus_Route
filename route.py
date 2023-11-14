import requests
import Constants

class Route:
    def __init__(self):
        self.api_url = "https://routes.googleapis.com/directions/v2:computeRoutes"
        self.api_key = Constants.map_api_key
        self.headers = {"Content-Type": "application/json", 
                        "X-Goog-Api-Key":self.api_key,
                        "X-Goog-FieldMask":"routes.duration,routes.distanceMeters,routes.polyline.encodedPolyline"}

    def fetchRoute(self, originLat, originLng, destLat, destLng, intermediatesLat=None, intermediatesLng=None):
        route_request = {"origin": {
                            "location":{
                                "latLng":{
                                    "latitude": originLat,
                                    "longitude": originLng,
                                    }
                                }
                            },
                         "destination": {
                                "location":{
                                    "latLng":{
                                        "latitude": destLat,
                                        "longitude": destLng
                                        }
                                }
                            },
                         "travelMode": "DRIVE",
                         "routingPreference": "TRAFFIC_AWARE",
                         "languageCode": "en_US",
                         "units": "IMPERIAL",
                }
       
        if intermediatesLat and intermediatesLng:
            waypoint = {
                "location": {
                    "latLng": {
                        "latitude": intermediatesLat,
                        "longitude": intermediatesLng
                    }
                }
            }
            route_request["intermediates"] = waypoint
          
        response = requests.post(self.api_url,headers=self.headers, json=route_request)  
        return response.json()


#fetchRoute = Route()

#response_data = fetchRoute.getRoute(40.820043999999996, -73.949822100000006, 40.82377614314247, -73.94502568555461)
#print(response_data)




