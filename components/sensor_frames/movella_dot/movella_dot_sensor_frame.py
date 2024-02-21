from customtkinter import CTkFrame, CTkTabview, CTkLabel, CTkFont, CTkComboBox, StringVar, CTkButton, CTkLabel,CTkInputDialog
import threading
from tkinter import TclError
from CTkMessagebox import CTkMessagebox

from components.sensor_frames.movella_dot import  movella_dot_left_frame as mdlf
from components.sensor_frames.movella_dot import  movella_dot_right_frame as mdrf

from components.sensor_frames.movella_dot import assign_sensor_window as asw
from components.sensor_frames.movella_dot import count_down_frame as cdf
from components.sensor_frames.movella_dot import plot_frame as pf

class MovellaDotSensorFrame(CTkFrame):
    def __init__(self, master, sensor_manager, console, params,   **kwargs):
        super().__init__(master,  **kwargs)

        self.console = console
        self.params = params
        self.sm = sensor_manager
        self.number_of_plot_points = 250

        self.sm.set_discovered_sensors_callback(self.discovered_senors)
        self.sm.set_connected_sensors_callback(self.connected_sensor)
        self.sm.set_battery_status_callback(self.battery_status_callback)
        self.sm.set_sensor_data_callback(self.on_sensor_data)
        self.sm.set_sensor_disconnected_callback(self.on_sensor_disconnected)
        self.sm.set_sensor_button_press_callback(self.on_sensor_button_press)

        self.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure((2), weight=1)
        self.grid_columnconfigure((0,1), weight=1)

        self.connected_sensor_positions = {}

        self.scan_btn =  CTkButton(self, text="scan", fg_color="#5D5FEF", command=self.scan_for_sensors, )
        self.scan_btn.grid(row=0, column=0, sticky='nw',  padx=5, pady=10 )
        
        self.left_frame = mdlf.MovellaDotLeftFrame(self, console, params, self.start_measuring_for_sensors, self.stop_measuring_for_sensors, self.set_protocol )
        self.left_frame.grid(row=2, column=0, padx=5, pady=10, sticky="nsew" )
        self.left_frame.grid_propagate(False)

        self.right_frame = mdrf.MovellaDotRightFrame(self, console, params, self.count_down_complete_ref)
        self.right_frame.grid(row=2, column=1, padx=5, pady=10, sticky="nsew" )
        self.right_frame.grid_propagate(False)

        # are added when connected and removed when disconnected
        self.connected_sensors = []
        self.connected_sensor_actions = []

        self.assign_sensor_window = None

        self.protocol = None
        self.is_manual = True
    
    def set_protocol(self, protocol):
        print(f"setting protocol to {protocol['name']}")
       
        self.protocol = protocol
        self.p_reps = protocol["repetitions"]
        self.reps = 1 # first rep
        self.reps_complete = 0
        reps_to_go = self.p_reps - self.reps_complete
        #self.left_frame.protcol_frame.status_label.configure(text=f'reps complete: {self.reps_complete}, reps to go: {reps_to_go} ')
        if(protocol["time_per_rep"]== 0):
            self.is_manual = True
        else:
            self.is_manual = False

        print("is manual", self.is_manual)
        self.right_frame.protocol_label.configure(text=protocol["name"])

    def scan_for_sensors(self):
        print(f"scan for sensors button pressed") 
        self.sm.manager.send_message("scan", {})
        #self.console.clear_console()
        self.console.insert_text("scanning for sensors ...") 

    def count_down_complete_ref(self, complete):
        if(complete):
            print(f"count down complete, load plot frame")
            self.right_frame.plot_frame.lift()

            # start the protocol timer if time_per_rep
            if(self.protocol["time_per_rep"]!=0):
                self.start_protcol_timer()
            else:
                print("manual stop for protcol")
                text = self.right_frame.protocol_label.cget('text')
                p_name = self.protocol["name"]
                text = f"{p_name} rep {self.reps}"
                self.right_frame.protocol_label.configure(text=text)
            

    def assign_sensor_ref(self, address, assignment):
        print(f"UI: {address} {assignment}")
        sensor = self.sm.manager.get_connected_sensor_by_address(address)
        sensor.set_placement(assignment)
        sensor_actions = [sa for sa in self.connected_sensor_actions if sa["address"] == address][0]

        if(sensor_actions["placement_label"] != None):
            sensor_actions["placement_label"].destroy()

        placement_label = CTkLabel(self.left_frame.sensor_frame, text=f"{assignment}")
        placement_label.grid(row=sensor_actions["position"]+2, column=6, sticky="nesw")
        placement_label.identifier = "placement_label"
        sensor_actions["placement_label"] = placement_label

    def on_sensor_button_press(self, address, press_type):
        if(press_type == 5):
            print(f"button press from {address}")
            if self.assign_sensor_window is None or not self.assign_sensor_window.winfo_exists():
                print("show top level window")
                self.assign_sensor_window = asw.AssignSensorWindow(self, address, self.assign_sensor_ref, self.params)  # create window if its None or destroyed
            else:
                self.assign_sensor_window.focus()  # if window exists focus it
            
   
    def connect_to_sensor(self, address, position):
        print(f"conecting to sensor {address} in position {position}")
        self.connect_to_pos = position
        self.connected_sensor_positions[address] = position
        self.sm.manager.send_message("connect", address)
        self.console.clear_console()
        self.console.insert_text(f"connecting to dot {address} ...") 

    
    def connected_sensor(self, sensor):
        print(f"UI connected to {sensor}")

        sensor_actions = {
            "address": sensor.address,
            "position": self.connect_to_pos,
            "connect_button" : None,
            "disconnect_button": None,
            "identify_button" : None,
            "batt_label" : None,
            "data_rate_label": None,
            "placement_label": None,
        }

      
        self.console.clear_console()
        self.console.insert_text("Connected to Dot: " + sensor.address + " " +'\n')

        #place the identify button over the connect button
        #self.connected_sensor_identity_button = CTkButton(self.left_frame, text="identify", fg_color="#5D5FEF", command= lambda: self.identify_sensor(sensor.address))
        connected_sensor_identity_button = CTkButton(self.left_frame.sensor_frame, text="identify", fg_color="#5D5FEF", command= lambda: self.identify_sensor(sensor.address))
        connected_sensor_identity_button.grid(row=self.connect_to_pos+2, column=1, padx=10, pady=10, sticky="nw")
        connected_sensor_identity_button.identifier = "indentify_btn"
        sensor_actions["identify_button"] = connected_sensor_identity_button

        connected_sensor_batt_label = CTkLabel(self.left_frame.sensor_frame, text=f"{sensor.batt_level}%", font=CTkFont(size=12, weight="bold"))
        connected_sensor_batt_label.grid(row=self.connect_to_pos+2, column=2, padx=10, pady=10, sticky="nw")
        connected_sensor_batt_label.identifier = "batt_status"
        sensor_actions['batt_label'] = connected_sensor_batt_label

        disconnect_sensor_btn = CTkButton(self.left_frame.sensor_frame, text="disconnect", command= lambda: self.disconnect_from_sensor(sensor.address))
        disconnect_sensor_btn.grid(row=self.connect_to_pos+2, column=3, padx=10, pady=10, sticky="nw")
        disconnect_sensor_btn.identifier = "disconnect_btn"
        sensor_actions['disconnect_button'] = disconnect_sensor_btn

        connected_sensor_data_rate_label = CTkLabel(self.left_frame.sensor_frame, text=f"60 Hz", font=CTkFont(size=12, weight="bold"))
        connected_sensor_data_rate_label.grid(row=self.connect_to_pos+2, column=4, padx=10, pady=10, sticky="nw")
        connected_sensor_data_rate_label.identifier = "data_rate"
        sensor_actions["data_rate_label"] = connected_sensor_data_rate_label

        self.connected_sensor_actions.append(sensor_actions)
    
    # no need for this function
    def on_sensor_data(self, data_packet):
        #print(data_packet.address, data_packet.data_packet)
        sensor = self.sm.manager.get_connected_sensor_by_address(data_packet.address)
        #print(found_sensor)
        #found_sensor.set_accleration([data_packet.data_packet[0][0], data_packet.data_packet[0][5], data_packet.data_packet[0][6], data_packet.data_packet[0][7] ])

    def update_stream_plot(self):

        thread = threading.Thread(target=self.clear_and_plot( self.right_frame.plot_frame.ax, self.right_frame.plot_frame.stream_fig_canvas, f"Acceleration",  self.sm.manager.get_connected_sensors()))
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

            sensor_actions = [sa for sa in self.connected_sensor_actions if sa["address"] == s.get_address()][0]
            sensor_actions["data_rate_label"].configure(text=f"{s.get_last_data_rate()} Hz")
            axis.plot(x, accel_x)
        
        canvas.draw()

    def stop_measuring_for_sensors(self):

        if(self.is_manual): # start and stop on our own
            print("should be here")

            self.reps_complete += 1
            self.reps += 1
            
       
            if(self.reps_complete == self.protocol["repetitions"]):
                p_name = self.protocol["name"]
                text = f"{p_name} complete"
                self.right_frame.protocol_label.configure(text=text)
                reps_to_go = self.p_reps - self.reps_complete
                self.left_frame.protcol_frame.update_status(f'reps complete: {self.reps_complete}, reps to go: {reps_to_go} ')
                
            else:
                
                reps_to_go = self.p_reps - self.reps_complete
                self.left_frame.protcol_frame.update_status(f'reps complete: {self.reps_complete}, reps to go: {reps_to_go} ')
                #self.left_frame.protcol_frame.complete_protocol()
                

        print(f"stop measuring on all sensors")
        self.after_cancel(self.update_stream_plot_task_id)
        for s in self.sm.manager.get_connected_sensors():
            print(s.get_packet_count(), s.get_last_data_rate())

        self.sm.manager.send_message("stop_measuring_all", {})
        self.console.clear_console()
        self.console.insert_text(f"stopping test...") 

    def start_protcol_timer(self):
        self.time_remaining = self.protocol["time_per_rep"]  # Reset the countdown time
        self.update_protocol_timer()

    def update_protocol_timer(self):
        protocol_name = self.protocol["name"]
        if self.time_remaining > 0:
            text = self.right_frame.protocol_label.cget('text')
            text = f"{protocol_name} time remaining {self.time_remaining} for rep {self.reps}"
            self.right_frame.protocol_label.configure(text=text)
            self.time_remaining -= 1
            self.protocol_countdown = self.after(1000, self.update_protocol_timer)
        else:
            #self.time_remaining -= 1
            text = f"{protocol_name} time remaining {self.time_remaining} for rep {self.reps}"
            self.right_frame.protocol_label.configure(text=text)

            self.stop_measuring_for_sensors()
            
            self.reps += 1
            self.reps_complete += 1
            print("reps complete", self.reps_complete)
            # initiate next rep (prob should sleep for a bit)
            if(self.reps_complete != self.protocol["repetitions"]):
                reps_to_go = self.p_reps - self.reps_complete
                self.left_frame.protcol_frame.update_status(f'reps complete: {self.reps_complete}, reps to go: {reps_to_go} ')
                self.start_measuring_for_sensors()
            else:
                text = f"{protocol_name} complete"
                self.right_frame.protocol_label.configure(text=text)
                
                reps_to_go = self.p_reps - self.reps_complete
                self.left_frame.protcol_frame.update_status(f'reps complete: {self.reps_complete}, reps to go: {reps_to_go} ')
                self.reps = self.protocol["repetitions"]

                #self.left_frame.protcol_frame.complete_protocol()

            


    def start_measuring_for_sensors(self):

        #make sure there are connected sensors and there is a protcol
        if(self.sm.manager.get_number_of_connected_sensors()>0 and self.protocol is not None):

            self.sm.manager.send_message("start_measuring_all", {})
            self.console.clear_console()
            self.console.insert_text(f"starting test...") 
            # initiate countdown
            self.right_frame.raise_frame(self.right_frame.count_down_frame)
            self.right_frame.count_down_frame.start_countdown()

            #protocol_label
            self.right_frame.protocol_label.configure(text=f"get ready for rep {self.reps}")
        
            self.right_frame.plot_frame.ax.clear()
            self.update_stream_plot()
        
            print(f"start measuring on all sensors")
        else:
            print(f"no connected sensors")
            if(self.sm.manager.get_number_of_connected_sensors()==0):
                CTkMessagebox(title="Error", message="No sensors connected", icon="cancel")
            

        

    def battery_status_callback(self, address, battery):
        print(f"ui batt status {address} {battery}%")

        if (len(self.connected_sensor_actions) == len(self.sm.manager.get_connected_sensors())):
           sensor_actions = [sa for sa in self.connected_sensor_actions if sa["address"] == address][0]
           sensor_actions['batt_label'].configure(text=f"{battery}%")
        #print(sensor_actions)
        #self.
        # to really use this we need to be able to track the rows / connected sensors to update the correct one
        #if hasattr(self, 'connected_sensor_batt_label'):
        #    sensor_actions['batt_label'].configure(text=f"{battery}%")
            #if(battery <= 10):
            #    self.connected_sensor_batt_label.configure(text=f"{battery}%", text_color="red")
            #    self.console.insert_text(f"sensor {address} battery 10% or less" + '\n\n') 
        #    self.console_frame.insert_text(f"sensor {address} will not send data" + '\n\n') 

    
    def identify_sensor(self, address):
        print(f"indentifying sensor {address}")
        self.sm.manager.send_message("identify", address)
        self.console.clear_console()
        self.console.insert_text(f"indentifying sensor {address} ..." ) 

    def on_sensor_disconnected(self, address):
        
        # need to remove all the buttons associated with connected and return to just connect
        pos = self.connected_sensor_positions[address]

        #sensor_actions = [sa for sa in self.connected_sensor_actions if sa["address"] == address][0]
        
        # position + 2 gets the row
        for widget in self.left_frame.sensor_frame.grid_slaves(row=pos+2):
           
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
                
                elif(widget.identifier == "placement_label"):
                     widget.destroy()

        print(f"sensor {address} disconnected ")

        
        sensor_action = [sa for sa in self.connected_sensor_actions if sa["address"] == address][0]
        self.connected_sensor_actions.remove(sensor_action)
        self.console.clear_console()
        self.console.insert_text(f"sensor {address} disconnected")

    def disconnect_from_sensor(self, address):
        #found_sensor = [sensor for sensor in self.sm.mangage.get_connected_sensors if sensor.address == address][0]
        #self.sm.connected_sensors.remove(found_sensor)
        self.sm.manager.send_message("disconnect", address)
        self.console.clear_console()
        self.console.insert_text(f"disconnecting sensor {address} ...")

    def discovered_senors(self, sensors):
        labels = []
        connect_buttons = []

        def connect_lambda(address, position):
            return lambda: self.connect_to_sensor(address, position)
        
        self.console.clear_console()

        if(len(sensors)>0):
            
            for idx, s in enumerate(sensors):
                self.console.insert_text("Sensor found: " + s.address + " " +'\n')
                label = CTkLabel(self.left_frame.sensor_frame, text=f"{s.address}")
                labels.append(label)
                connect_button = CTkButton(self.left_frame.sensor_frame, text="connect", fg_color="#EF5DA8", command=connect_lambda(s.address, idx))
                connect_buttons.append(connect_button) 

            for i in range(len(labels)):
                labels[i].grid(row=i+2, column=0, padx=10,pady=10, sticky="w")
                connect_buttons[i].grid(row=i+2, column=1, padx=10, pady=10, sticky="w")  
        else:
            self.console.insert_text("No sensors found")
        

        