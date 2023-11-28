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
        thresholds = [49, 99, 149, 199, 249, 299, 349, 399, 449, 499, 549, 599, 649, 699, 749, 799, 849, 899,
                      949, 999, 1049, 1099, 1149, 1199, 1249, 1299, 1349]
        delta_values = [-44, -32, -21, -9, 2, 14, 25, 37, 49, 60, 72, 84, 96, 107, 119, 131, 142, 154, 166, 178,
                        189, 201, 213, 225, 236, 248, 260]

        delta = 0
        for i, threshold in enumerate(thresholds):
            if self.distance <= threshold:
                return int(delta_values[i])



    def find_w125_to_nac_delta(self):

    def find_w145_to_nac_delta(self):
        thresholds = [49, 99, 149, 199, 249, 299, 349, 399, 449, 499, 549, 599, 649, 699, 749, 799, 849, 899]
        delta_values = [4, 17, 29, 42, 54, 67, 79, 91, 104, 116, 129, 141, 154, 166, 179, 191, 204, 216]

        delta = 0
        for i, threshold in enumerate(thresholds):
            if self.distance <= threshold:
                delta = delta_values[i]
        return delta