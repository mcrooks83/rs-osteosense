from sensor_sdk import helper_functions as hf

class BatteryStatus:
    def __init__(self, battery_level, is_charging):
        self.battery_level = battery_level
        self.is_charging = is_charging

class SensorDataPacket:
    def __init__(self, address, data_packet):
        self.address = address
        self.data_packet = data_packet

class MessageError:
    def __init__(self, error_message):
        self.error_message

## Sensor Classes
class ScannedSensor:
    def __init__(self, address, ble_address, ble_device):
        self.address = address
        self.ble_address = ble_address
        self.ble_device = ble_device
    def get_scanned_sensor_address(self):
        return self.address
    def get_scanned_sensor_ble_device(self):
        return self.ble_device
    
class ConnectedSensor:
    def __init__(self, address, client, ble_device, sensor_manager):
        self.address = address
        self.ble_device = ble_device
        self.ble_client = client
        self.sensor_manager = sensor_manager
        self.batt_level = 0
        self.raw_data = []
        self.data_rate = 0
        self.packet_count = -1
        self.time_pc = []
        self.accel_x = []

        #vars
        self.prev_timestamp = 0
        self.latest_timestamp = 0

    def on_sensor_data(self, sender, data):
        
        encoded_data = hf.encode_data_packet(data)
        
        data_packet = SensorDataPacket(self.address, encoded_data)
        self.sensor_manager.on_sensor_data(data_packet)
        
        self.latest_timestamp = encoded_data[0][0] 
        if(self.prev_timestamp != 0):
            self.update_data_rate(int( 1/((self.latest_timestamp - self.prev_timestamp)/1e6)))
            self.prev_timestamp = self.latest_timestamp
        else:
            self.prev_timestamp = self.latest_timestamp 

        self.add_raw_data_packet(encoded_data)
        self.accel_x.append(encoded_data[0][5])
        self.time_pc.append(self.packet_count)
        self.packet_count +=1
        
    def on_battery_status_update(self, sender, batt):
        battery_level = hf.get_battery_level(batt)
        self.batt_level = battery_level.battery_level
        self.sensor_manager.on_battery_status(self.address, battery_level.battery_level)
    

    def clear_all_data(self):
        self.raw_data = []
        self.packet_count = -1
        self.time_pc = []
        self.accel_x = []

    def get_address(self):
        return self.address
    
    def update_data_rate(self, rate):
        # compute the data rate from timestamps
        self.data_rate = rate

    def get_batt_level(self):
        return self.batt_level
    
    def get_last_data_rate(self):
        return self.data_rate
    
    def add_raw_data_packet(self, data_packet):
        self.raw_data.append(data_packet)

    def get_raw_data(self, num_of_points):
        return self.raw_data[-num_of_points:]
    
    def get_packet_count(self):
        return self.packet_count
    
    def get_accel_x(self, num_of_points):
        return self.accel_x[-num_of_points:]
    
    def get_time_pc(self, num_of_points):
        return self.time_pc[-num_of_points:]

    def remove_raw_data(self):
        self.raw_data = []

