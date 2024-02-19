

class Sensor:
    def __init__(self, address):
        self.address = address
        self.packet_count = 0
        self.time = []
        self.accel_x = []
        self.accel_y = []
        self.accel_z = []
        self.date_rate  = 60
        self.prev_timestamp = 0


    def set_accleration(self, data):
        self.time.append(self.packet_count)
        self.accel_x.append(data[1])
        self.accel_y.append(data[2])
        self.accel_z.append(data[3])
        self.packet_count +=1 

    def get_acceleration(self, num_of_points):
        return [self.time[-num_of_points:], self.accel_x[-num_of_points:], self.accel_y[-num_of_points:], self.accel_z[num_of_points:]]

    def get_packet_count(self):
        return self.packet_count
    
    def compute_data_rate(self):
        pass
    def compute_loading_intensity(self):
        pass
    def compute_alogirhtm(self):
        pass