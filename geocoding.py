import requests
import Constants

class Geocoding:
    def __init__(self):
        self.api_url = "https://maps.googleapis.com/maps/api/geocode/json"
        self.api_key = Constants.MAP_API_KEY
    
    def fetch_coordinates(self, street_address, street_name, city = "New York", state = "NY"):
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
       
#test = Geocoding()
#result = test.fetchLatLng(418, "W 145th St")
#lat = result['lat']
#lng = result['lng']
#print(lat, lng)