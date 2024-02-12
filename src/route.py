import requests
import os

from dotenv import load_dotenv

load_dotenv()
"""
A class to interact with the Google Maps Directions API for computing routes.

Attributes:
    api_url (str): The URL for the Google Maps Directions API.
    api_key (str): The API key for accessing the Google Maps Directions API.
    headers (dict): The headers to be included in the API request.

Methods:
    fetch_route: Sends a request to the Google Maps Directions API to compute a route.

Example:
    route = Route()
    response_data = route.fetch_route(40.819557163853155, -73.94991793531442, 40.82377614314247, -73.94502568555461)
"""

# Future Suggestion change "travelMode": "WALK" and remove "routingPreference" to reduce api cost, then
# Train Machine Learning Model to reduce the API duration 

class Route:
    def __init__(self):
        """
        Initialize the Route class.

        Sets up the API URL, API key, and headers for API requests.
        """
        self.api_url = "https://routes.googleapis.com/directions/v2:computeRoutes"
        self.api_key = os.getenv('MAP_API_KEY')

        # Define header for api request
        self.headers = {"Content-Type": "application/json", 
                        "X-Goog-Api-Key":self.api_key,
                        "X-Goog-FieldMask":"routes.duration,routes.distanceMeters,routes.polyline.encodedPolyline"}

    def fetch_route(self, origin_latitude, origin_longitude, destination_latitude, destination_longitude, intermediates_latitude=None, intermediates_longitude=None):
        """
        Fetches a route from the Google Maps Route API.

        Args:
            origin_latitude (float): The latitude of the starting point.
            origin_longitude (float): The longitude of the starting point.
            destination_latitude (float): The latitude of the destination.
            destination_longitude (float): The longitude of the destination.
            intermediates_latitude (float): The latitude of intermediate points (optional).
            intermediates_longitude (float): The longitude of intermediate points (optional).

        Returns:
            dict: The response data from the Google Maps Route API.
                  Returns None if there is an error in the API request.
        """
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

    origin_latitude = 40.8103721597239 
    origin_longitude = -73.95278450679731

    destination_latitude = 40.819557163853155
    destination_longitude = -73.94991793531442
    
    intermediates_latitude = None
    intermediates_longitude = None
    
    response_data = fetchRoute.fetch_route(origin_latitude, origin_longitude, destination_latitude, destination_longitude, intermediates_latitude, intermediates_longitude)
    print(response_data)




