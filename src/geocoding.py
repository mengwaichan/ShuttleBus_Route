import requests
import os
from dotenv import load_dotenv

load_dotenv()
"""
A class for geocoding street addresses to geographical coordinates using the Google Maps Geocoding API.

Attributes:
    api_url (str): The URL for the Google Maps Geocoding API.
    api_key (str): The API key for accessing the Google Maps Geocoding API.

Methods:
    fetch_coordinates: Fetches the geographical coordinates for a given street address.

Example:
    geocoder = Geocoding()
    result = geocoder.fetch_coordinates(685, "St Nicholas Ave")
    lat, lng = result['lat'], result['lng']
"""
class Geocoding:
    def __init__(self):
        """
        Initializes the Geocoding class with the API URL and key.
        """
        self.api_url = "https://maps.googleapis.com/maps/api/geocode/json"
        self.api_key = os.getenv('MAP_API_KEY')
    
    def fetch_coordinates(self, street_address, street_name, city = "New York", state = "NY"):
        """
        Fetches the geographical coordinates for a given street address.

        Args:
            street_number (int): The street number.
            street_name (str): The street name.
            city (str): The city (default is "New York").
            state (str): The state (default is "NY").

        Returns:
            dict: A dictionary containing the latitude and longitude.
                  Returns None if there is an error in the API request.
        """
        address = str(street_address) + " " + street_name + ", " + city + ", " + state 
        params = {
            "address": address,
            "key": self.api_key
        }
        response = requests.get(self.api_url, params=params)
        if response.status_code == 200 and response.json()['status'] == 'OK':
            location = response.json()['results'][0]['geometry']['location']
            return location
            
        else:
            print("Error:", response.json()['status'])
            return None

# For testing purpose
# To test run 'python geocoding.py' in terminal
if __name__== '__main__':       
    test = Geocoding()
    result = test.fetch_coordinates(685,"St Nicholas Ave")
    lat = result['lat']
    lng = result['lng']
    print(lat, lng)