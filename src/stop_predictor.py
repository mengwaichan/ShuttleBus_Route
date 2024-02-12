from src.bus_stop import BusStop
"""
A class to predict the next bus stop based on Airtag data.

Attributes:
    street_name (str): The name of the street where the bus is located.
    street_address (str): The street address of the bus location.
    time_difference (float): The time difference between current and previous Airtag timestamps.
    previous_route (BusRoute): The previous route object for synchronization.
    interest_a (str): Area of interest for route prediction.

Methods:
    get_last_destination: Retrieves the last location the bus was headed.
    get_next_stop: Predicts the next bus stop based on current conditions.
    reached_w145: Checks if the bus has reached W145.
    reached_w125: Checks if the bus has reached W125.
    reached_ccny: Checks if the bus has reached The City College of New York.
    skipped_stop: Handles cases where the bus skipped a stop.
"""

# All Bus Stops and Intermediates shuttle bus will pass 
BUS_STOPS = {
    'W145': BusStop(1, "W145", 40.82377614314247, -73.94502568555461, 691, "St Nicholas Ave"),  # 691 St Nicholas Ave
    'NAC': BusStop(2, "NAC", 40.819557163853155, -73.94991793531442, 201, "Convent Ave"),  # 201 The City College of New York
    'W125': BusStop(3, "W125", 40.8103721597239, -73.95278450679731, 284, "St Nicholas Ave"),  # 284 St Nicholas Ave # W 124th St
    'intermediate_to_125': BusStop(4, "intermediate_125", 40.810976077358795, -73.95405670678701),
    'intermediate_to_nac': BusStop(5, "intermediate_nac", 40.811255, -73.953659),
    'intermediate_145_nac': BusStop(6, "intermediate_145_nac", 40.821392729005844, -73.9463009155883),
    'intermediate_nac_145': BusStop(7, "intermediate_nac_145", 40.821385, -73.948542)
}

class StopPredictor:
    def __init__(self, street_name, street_address, interest_a, time_difference, previous_route = None):
        # Input
        self.street_name = street_name
        self.street_address = street_address
        self.time_difference = time_difference
        self.previous_route = previous_route
        self.interest_a = interest_a

        # Output
        self.next_stop = None
        self.previous_stop = None
        self.intermediate = None
        self.delta = 0
    
    def get_last_destination(self):
        if not self.previous_route:
            self.next_stop = BUS_STOPS['NAC']
            return
        else:
            self.next_stop = self.previous_route.next_stop
            self.intermediate = self.previous_route.intermediate

        # Get Previous Stop based on Previous Route
        if self.previous_route:
            self.previous_stop = self.previous_route.previous_stop
        else:
            self.previous_stop = BUS_STOPS['NAC']

    def get_next_stop(self):
        if self.reached_w145():
            return
        if self.reached_w125():
            return
        if self.reached_ccny():
            return
        
        # if airtag did not update at the bus stop
        if self.previous_route:
            self.skipped_stop()
            return

    # Bus has reached a station
    def reached_w145(self):
        is_w145 = ((int(self.street_address) >= 600 and self.street_name == "St Nicholas Ave") or 
                   (self.interest_a == "145 St" and self.street_address == "") or
                   self.street_name in ["W 145th St", "W 141st St"])

        if is_w145:
            if self.street_name == "W 145th St":
                self.next_stop = BUS_STOPS['NAC']
                self.previous_stop = BUS_STOPS['W145']
                self.intermediate = BUS_STOPS['intermediate_145_nac']
                self.delta = 180
                return True
            else: 
                self.next_stop = BUS_STOPS['NAC']
                self.previous_stop = BUS_STOPS['W145']
                self.intermediate = None
                self.delta = 60
                return True
        return False

    def reached_w125(self):
        is_w125 = ((100 <= int(self.street_address) <= 300 and self.street_name == "St Nicholas Ave") or 
                   self.street_name in ["Hancock Pl", "W 124th St", "Manhattan Ave", "W 125th St"] or 
                   self.interest_a == "Hancock Park")
        
        if is_w125:
            self.next_stop = BUS_STOPS['NAC']
            self.intermediate = BUS_STOPS['intermediate_to_nac']
            self.previous_stop = BUS_STOPS['W125']
            self.delta = 60
            return True
        
        # Special Case
        if int(self.street_address) == 0 and self.street_name == "St Nicholas Ave":
            if self.interest_a == "125 St":
                self.next_stop = BUS_STOPS['NAC']
                self.intermediate = BUS_STOPS['intermediate_to_nac']
                self.previous_stop = BUS_STOPS['W125']
                self.delta = 60
                return True
            else:
                self.next_stop = BUS_STOPS['NAC']
                self.previous_stop = BUS_STOPS['W145']
                self.intermediate = None
                self.delta = 180
                return True
            
        if int(self.street_address) <= 157 and self.street_name == "Morningside Ave" and self.previous_stop == ['NAC']:
            self.next_stop = BUS_STOPS['NAC']
            self.intermediate = BUS_STOPS['intermediate_to_nac']
            self.previous_stop = BUS_STOPS['W125']
            self.delta = 60
            return True
        return False

    def reached_ccny(self):
        is_ccny = (((150 <= int(self.street_address) <= 210)  and self.street_name == "Convent Ave") or 
                   (self.interest_a == "The City College of New York" and self.street_address == ""))
       
        if is_ccny: # CCNY
            if 780 <= self.time_difference <= 1020:
                if self.previous_route.next_stop == BUS_STOPS['W125']: # going to w145
                    self.next_stop = BUS_STOPS['W145']
                    self.previous_stop = BUS_STOPS['NAC']
                    self.intermediate = BUS_STOPS['intermediate_nac_145']
                    self.delta = 240
                    return True
                elif self.previous_route.next_stop == BUS_STOPS['W145']: # going to w125
                    self.next_stop = BUS_STOPS['W125']
                    self.intermediate = BUS_STOPS['intermediate_to_125']
                    self.previous_stop = BUS_STOPS['NAC']
                    self.delta = 240
                    return True
            if self.previous_stop == BUS_STOPS['W125']: # going to w145
                self.next_stop = BUS_STOPS['W145']
                self.previous_stop = BUS_STOPS['NAC']
                self.intermediate = BUS_STOPS['intermediate_nac_145']
                self.delta = 240
                return True
            elif self.previous_stop == BUS_STOPS['W145']: # going to w125
                self.next_stop = BUS_STOPS['W125']
                self.intermediate = BUS_STOPS['intermediate_to_125']
                self.previous_stop = BUS_STOPS['NAC']
                self.delta = 240
                return True
        return False
    
        # Handle Cases Based on where the bus is
   
    def skipped_stop(self):
        is_w145_route = (((249 < int(self.street_address) <= 360 and self.street_name == "Convent Ave") or 
                          self.street_name in ["W 140th St", "W 141st St", "W 142nd St", "W 143rd St", "W 144th St"])
                        )

        is_w125_route = (((135 >= int(self.street_address) and self.street_name == "Convent Ave") or self.street_name == "Morningside Ave" or 
                         self.street_name in ["W 135th St", "W 133rd St", "W 131st St", "W 130th St", "W 129th St", "W 128th St", "W 127th St", "W 126th St"]) 
                        )

        if is_w145_route and self.previous_route.previous_stop == BUS_STOPS['W125']:
            self.next_stop = BUS_STOPS['W145']
            self.previous_stop = BUS_STOPS['NAC']
            return
        
        if is_w125_route:
            if self.previous_route.previous_stop == BUS_STOPS['W145']:
                self.next_stop = BUS_STOPS['W125']
                self.previous_stop = BUS_STOPS['NAC']
                self.intermediate = BUS_STOPS['intermediate_to_125']
                return
            elif self.previous_route.next_stop == BUS_STOPS['W145']:
                self.next_stop = BUS_STOPS['W125']
                self.previous_stop = BUS_STOPS['NAC']
                self.intermediate = BUS_STOPS['intermediate_to_125']
                return
    