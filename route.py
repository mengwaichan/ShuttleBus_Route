import requests
import Constants

class Route:
    def __init__(self):
        self.api_url = "https://routes.googleapis.com/directions/v2:computeRoutes"
        self.api_key = Constants.route_api_key
        self.headers = {"Content-Type": "application/json", "X-Goog-Api-Key":self.api_key,"X-Goog-FieldMask":"routes.duration,routes.distanceMeters"}

    def getRoute(self, originLat, originLng, destLat, destLng, intermediatesLat=None, intermediatesLng=None):
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

#response_data = fetchRoute.getRoute(40.8103721597239, -73.95278450679731, 40.819557163853155, -73.94991793531442)
#print(response_data)




