from sensor_sdk import helper_functions as hf
import threading
from Algorithms import compute_weight_bearing as cwb
import queue
import multiprocessing
import time
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
        self.placement = ""
        self.sensor_manager = sensor_manager
        self.batt_level = 0
        self.raw_data = []
        self.data_rate = 0
        self.packet_count = 0
        self.time_pc = []
        self.accel_x = []
        self.li = [] #loading intensity
        self.rf = [] # reaction force
        self.data_in_window = []
        self.time_idx = 0
        self.time_idx_for_window = []
        self.set_data_rate = 60
        self.is_measuring = False
        self.is_first_data_packet = True

        #vars
        self.prev_timestamp = 0
        self.latest_timestamp = 0

        # alogrithm details
        self.window_width = 5 #seconds
        self.data_window = self.set_data_rate * 5 # data rate * window seconds

        self.result_queue = multiprocessing.Queue()
        
    def set_is_measuring(self, is_measuring):
        self.is_measuring = is_measuring

    def on_button_event(self,sender, event):
        press_type = event[0] # should be 5 for single press
        if(press_type == 5):
            print(f"single button press from {self.address}")
            self.sensor_manager.on_sensor_button_press(self.address, press_type)

    def on_sensor_data(self, sender, data):

        # if its the first packet ignore it
        if(self.is_first_data_packet):
            self.is_first_data_packet = False
        else:
            encoded_data = hf.encode_data_packet(data)
        
            self.latest_timestamp = encoded_data[0][0] 
            if(self.prev_timestamp != 0):
                self.update_data_rate(int( 1/((self.latest_timestamp - self.prev_timestamp)/1e6)))
                self.prev_timestamp = self.latest_timestamp
            else:
                self.prev_timestamp = self.latest_timestamp 

            self.add_raw_data_packet(list(encoded_data[0]))
            self.data_in_window.append(list(encoded_data[0]))
            self.packet_count +=1

        # try to compute loading intensity
        if len(self.data_in_window) == self.data_window:            
            process = multiprocessing.Process(target=cwb.process_data_in_window, args=[self.data_in_window, self.set_data_rate, self.result_queue])
            process.start()
            self.after(1, self.check_process_result, process, self.result_queue)
            self.data_in_window = []
       
    def check_process_result(self, process, result_queue):
        try:
            data = result_queue.get(block=False)
            self.li.append(data["LI"])
            self.rf.append(data["RF"])
            self.time_idx_for_window.append(self.time_idx)
            self.time_idx += 1
            
        except queue.Empty:
            self.after(1, self.check_process_result, process, self.result_queue)

    # custom after function
    def after(self, time_sleep, func, arg1, arg2):
        time.sleep(time_sleep)
        func(arg1, arg2)

    def on_battery_status_update(self, sender, batt):
        battery_level = hf.get_battery_level(batt)
        self.batt_level = battery_level.battery_level
        self.sensor_manager.on_battery_status(self.address, battery_level.battery_level)
    

    def clear_all_data(self):
        self.raw_data = []
        self.packet_count = 0
        self.time_pc = []
        self.accel_x = []
        self.time_idx_for_window = []
        self.time_idx = 0
        self.li = []
        self.rf = []

    def get_address(self):
        return self.address
    
    def get_placement(self):
        return self.placement
    
    def set_placement(self, placement):
        self.placement = placement
    
    def set_set_data_rate(self, rate):
        self.set_data_rate = rate
    
    def get_set_data_rate(self):
        return self.set_data_rate
    
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
    
    def get_data_in_window(self):
        return self.data_in_window

    def clear_data_in_window(self):
        self.data_in_window = []
    
    def get_packet_count(self):
        return self.packet_count
    
    def get_length_raw_data(self):
        return len(self.raw_data)
    
    def get_accel_x(self, num_of_points):
        return self.accel_x[-num_of_points:]

    def get_li(self, num_of_points):
        return self.li[-num_of_points:]
    
    def get_time_pc(self, num_of_points):
        return self.time_pc[-num_of_points:]
    
    def get_time_idx_in_window(self, num_of_points):
        return self.time_idx_for_window[-num_of_points:]

    def remove_raw_data(self):
        self.raw_data = []
