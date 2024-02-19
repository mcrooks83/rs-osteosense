from customtkinter import CTkFrame, CTkTabview, CTkLabel, CTkFont, CTkComboBox, StringVar, CTkButton, CTkLabel
#from matplotlib.pyplot import Figure
#from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
#from matplotlib import style
#from mpl_toolkits.axisartist.axislines import AxesZero
#style.use('fivethirtyeight')
#style.use("dark_background")
import threading
import multiprocessing
import math
from tkinter import TclError

from components.sensor_frames.movella_dot import  movella_dot_left_frame as mdlf
from components.sensor_frames.movella_dot import  movella_dot_right_frame as mdrf

import classes.Sensor as s

class MovellaDotSensorFrame(CTkFrame):
    def __init__(self, master, sensor_manager, console, params,  **kwargs):
        super().__init__(master,  **kwargs)

        self.console = console
        self.params = params
        self.sm = sensor_manager

        #self.rate = 60
        self.number_of_plot_points = 250

        self.sm.set_discovered_sensors_callback(self.discovered_senors)
        self.sm.set_connected_sensors_callback(self.connected_sensor)
        self.sm.set_battery_status_callback(self.battery_status_callback)
        self.sm.set_sensor_data_callback(self.on_sensor_data)
        self.sm.set_sensor_disconnected_callback(self.on_sensor_disconnected)

        self.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure((2), weight=1)
        self.grid_columnconfigure((0,1), weight=1)

        self.connected_sensor_positions = {}

        self.scan_btn =  CTkButton(self, text="scan", command=self.scan_for_sensors, )
        self.scan_btn.grid(row=0, column=0, sticky='nw',  padx=5, pady=10 )

        self.button_frame = CTkFrame(self)
        self.button_frame.grid(row=3, column=0,  sticky='nw', padx=5, pady=10)
        self.button_frame.grid_rowconfigure(0, weight=1)

        self.start_measuring_btn =  CTkButton(self.button_frame, text="start test", fg_color="#5D5FEF", command=self.start_measuring_for_sensors )
        self.start_measuring_btn.grid(row=0, column=1, sticky='nw',  padx=5, pady=10 )

        self.stop_measuring_btn =  CTkButton(self.button_frame, text="stop test", fg_color="#5D5FEF", command=self.stop_measuring_for_sensors )
        self.stop_measuring_btn.grid(row=0, column=2, sticky='nw',  padx=5, pady=10 )
        
        self.left_frame = mdlf.MovellaDotLeftFrame(self, console, params)
        self.left_frame.grid(row=2, column=0, padx=5, pady=10, sticky="nsew" )
        self.left_frame.grid_propagate(False)

        self.right_frame = mdrf.MovellaDotRightFrame(self, console, params)
        self.right_frame.grid(row=2, column=1, padx=5, pady=10, sticky="nsew" )
        self.right_frame.grid_propagate(False)

        # are added when connected and removed when disconnected
        self.connected_sensors = []
    
    def scan_for_sensors(self):
        print(f"scan for sensors button pressed") 
        self.sm.manager.send_message("scan", {})
        #self.console.clear_console()
        self.console.insert_text("scanning for sensors ...") 

    def connect_to_sensor(self, address, position):
        print(f"conecting to sensor {address} in position {position}")
        self.connect_to_pos = position
        self.connected_sensor_positions[address] = position
        self.sm.manager.send_message("connect", address)
        self.console.clear_console()
        self.console.insert_text(f"connecting to dot {address} ...") 
    
    def connected_sensor(self, sensor):
        print(f"UI connected to {sensor}")
        #grid_info = get_label_row(label1)
        self.console.clear_console()
        self.console.insert_text("Connected to Dot: " + sensor.address + " " +'\n')

        self.connected_sensors.append(s.Sensor(sensor.address))

        #place the identify button over the connect button
        self.connected_sensor_identity_button = CTkButton(self.left_frame, text="identify", fg_color="#5D5FEF", command= lambda: self.identify_sensor(sensor.address))
        self.connected_sensor_identity_button.grid(row=self.connect_to_pos+2, column=1, padx=10, pady=10, sticky="nw")
        self.connected_sensor_identity_button.identifier = "indentify_btn"

        self.connected_sensor_batt_label = CTkLabel(self.left_frame, text=f"{sensor.batt_level}%", font=CTkFont(size=12, weight="bold"))
        self.connected_sensor_batt_label.grid(row=self.connect_to_pos+2, column=2, padx=10, pady=10, sticky="nw")
        self.connected_sensor_batt_label.identifier = "batt_status"

        self.disconnect_sensor_btn = CTkButton(self.left_frame, text="disconnect", command= lambda: self.disconnect_from_sensor(sensor.address))
        self.disconnect_sensor_btn.grid(row=self.connect_to_pos+2, column=3, padx=10, pady=10, sticky="nw")
        self.disconnect_sensor_btn.identifier = "disconnect_btn"

        self.connected_sensor_data_rate_label = CTkLabel(self.left_frame, text=f"60 Hz", font=CTkFont(size=12, weight="bold"))
        self.connected_sensor_data_rate_label.grid(row=self.connect_to_pos+2, column=4, padx=10, pady=10, sticky="nw")
        self.connected_sensor_batt_label.identifier = "data_rate"

    
    # no need for this function
    def on_sensor_data(self, data_packet):
        #print(data_packet.address, data_packet.data_packet)
        sensor = self.sm.manager.get_connected_sensor_by_address(data_packet.address)
        #print(found_sensor)
        #found_sensor.set_accleration([data_packet.data_packet[0][0], data_packet.data_packet[0][5], data_packet.data_packet[0][6], data_packet.data_packet[0][7] ])

    def update_stream_plot(self):

        thread = threading.Thread(target=self.clear_and_plot( self.right_frame.ax, self.right_frame.stream_fig_canvas, f"Acceleration",  self.sm.manager.get_connected_sensors()))
        thread.start()
        thread.join()
        #self.ax, self.stream_fig_canvas, f"Acceleration {self.c.data_rate} Hz", "packet count", x, acc_x, acc_y, acc_z )
        #threads = [threading.Thread(target=self.clear_and_plot, args=(self.right_frame.ax, self.right_frame.stream_fig_canvas,f"Acceleration", s), name=f"Thread-{s.address}") for s in self.connected_sensors]

        #for thread in threads:
        #    thread.start()

        # Wait for all threads to finish
        #for thread in threads:
        #    thread.join()

        self.update_stream_plot_task_id = self.after(1, self.update_stream_plot)
    
    def clear_and_plot(self, axis, canvas, title,  sensors_to_plot):
       
        axis.clear()
        axis.set_title(title)
        axis.set_xlabel("packet count")
       # axis.text(0.005, 1.05, f"Data Rate: {self.rate} Hz ", transform=axis.transAxes)
        num_of_points = self.number_of_plot_points
        
        for idx, s in enumerate(sensors_to_plot):
        #    print(s.get_packet_count())
            x = s.get_time_pc(num_of_points)
            accel_x = s.get_accel_x(num_of_points)
            #axis.text(0.005, 1.05 + (idx / 10), f"Data Rate: {s.get_last_data_rate()} Hz ", transform=axis.transAxes)
            self.connected_sensor_data_rate_label.configure(text=f"{s.get_last_data_rate()} Hz")
            axis.plot(x, accel_x)
        
        canvas.draw()

    def stop_measuring_for_sensors(self):
        print(f"stop measuring on all sensors")
        #self.after_cancel(self.update_stream_plot_task_id)
        for s in self.sm.manager.get_connected_sensors():
            print(s.get_packet_count(), s.get_last_data_rate())

        self.sm.manager.send_message("stop_measuring_all", {})
        self.console.clear_console()
        self.console.insert_text(f"stopping test...") 

    def start_measuring_for_sensors(self):
    
        self.right_frame.ax.clear()
        self.update_stream_plot()
       
        print(f"start measuring on all sensors")

        self.sm.manager.send_message("start_measuring_all", {})
        self.console.clear_console()
        self.console.insert_text(f"starting test...") 

    def battery_status_callback(self, address, battery):
        print(f"ui batt status {address} {battery}%")
        # to really use this we need to be able to track the rows / connected sensors to update the correct one
        #self.connected_sensor_batt_label.configure(text=f"{battery}%")
        #if(battery <= 10):
        #    self.console_frame.insert_text(f"sensor {address} battery 10% or less" + '\n\n') 
        #    self.console_frame.insert_text(f"sensor {address} will not send data" + '\n\n') 

    
    def identify_sensor(self, address):
        print(f"indentifying sensor {address}")
        self.sm.manager.send_message("identify", address)
        self.console.clear_console()
        self.console.insert_text(f"indentifying sensor {address} ..." ) 

    def on_sensor_disconnected(self, address):
        
        # need to remove all the buttons associated with connected and return to just connect
        pos = self.connected_sensor_positions[address]
        # position + 2 gets the row
        for widget in self.left_frame.grid_slaves(row=pos+2):

            #w_name = self.nametowidget(widget)
           
            if(hasattr(widget, "identifier")): 
                if(widget.identifier == "indentify_btn"):
                    print("destroying indentify button")
                    if widget.winfo_exists():
                        widget.destroy()
                    else:
                        print("The button does not exist.")

                # error here for some unknown reason
                elif(widget.identifier == "disconnect_btn"):
                    print("destroying disconnect button")
                    try:
                        if widget.winfo_exists():
                            widget.destroy()
                    except TclError as e:
                        print(f"Error while destroying the button: {e}")
                    
                    
                elif(widget.identifier == "batt_status"):
                     widget.destroy()

                elif(widget.identifier == "data_rate"):
                     widget.destroy()

        print(f"sensor {address} disconnected ")
        self.console.clear_console()
        self.console.insert_text(f"sensor {address} disconnected")

    def disconnect_from_sensor(self, address):
        found_sensor = [sensor for sensor in self.connected_sensors if sensor.address == address][0]
        self.connected_sensors.remove(found_sensor)
        self.sm.manager.send_message("disconnect", address)
        self.console.clear_console()
        self.console.insert_text(f"disconnecting sensor {address} ...")

    def discovered_senors(self, sensors):
        labels = []
        connect_buttons = []
        battery_labels = []

        def connect_lambda(address, position):
            return lambda: self.connect_to_sensor(address, position)
        
        self.console.clear_console()

        if(len(sensors)>0):
            
            for idx, s in enumerate(sensors):
                self.console.insert_text("Sensor found: " + s.address + " " +'\n')
                label = CTkLabel(self.left_frame, text=f"{s.address}")
                labels.append(label)
                connect_button = CTkButton(self.left_frame, text="connect", fg_color="#EF5DA8", command=connect_lambda(s.address, idx))
                connect_buttons.append(connect_button) 

            for i in range(len(labels)):
                labels[i].grid(row=i+2, column=0, padx=10,pady=10, sticky="w")
                connect_buttons[i].grid(row=i+2, column=1, padx=10, pady=10, sticky="w")  
        else:
            self.console.insert_text("No sensors found")
        

        