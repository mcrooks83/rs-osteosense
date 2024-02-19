class Parameters:

    def __init__(self):
        self.selected_sensor = ""


    def set_selected_sensor(self, selected_sensor):
        self.selected_sensor = selected_sensor
        
    def get_selected_sensor(self):
        return self.selected_sensor