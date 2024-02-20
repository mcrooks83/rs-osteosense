class Parameters:

    def __init__(self):
        self.selected_sensor = ""

        # note these are actually set by the assessment data that is returned (possibly by protocol)
        self.placements = [
            "left lower limb",
            "right lower limb",
            "waist",
            "upper spine",
            
        ]


    def get_placements(self):
        return self.placements
    
    def set_selected_sensor(self, selected_sensor):
        self.selected_sensor = selected_sensor
        
    def get_selected_sensor(self):
        return self.selected_sensor