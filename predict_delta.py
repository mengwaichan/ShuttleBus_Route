from joblib import load

class Predict_Delta:
    def __init__(self, distance, previous_stop, next_stop):
        self.distance = distance
        self.previous_stop = previous_stop
        self.next_stop = next_stop

        self.delta = 0
    
    def calculate_delta(self):
        if self.next_stop == "W145":
            self.delta = find_w145_delta()
            return
        
        if self.next_stop == "W125":
            self.delta = find_w125_delta()
            return
        
        if self.next_stop == "NAC":
            if self.previous_stop == "W145":
                self.delta = find_w145_to_nac_delta()
                return
            if self.previous_stop == "W125":
                self.delta = find_w125_to_nac_delta()
                return

    def find_w145_delta(self):

    def find_w125_delta(self):

    def find_w125_to_nac_delta(self):

    def find_w145_to_nac_delta(self):