import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import threading
import time

class FlightComputerUI:
    def __init__(self, flight_computer):
        self.flight_computer = flight_computer
        
        # Main window setup
        self.root = tk.Tk()
        self.root.title("Flight Computer Control Panel")
        self.root.geometry("1200x800")
        
        # Create notebook for multiple tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both')
        
        # Sensor Data Tab
        self.sensor_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.sensor_tab, text="Sensor Data")
        
        # Reaction Wheel Control Tab
        self.reaction_wheel_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.reaction_wheel_tab, text="Reaction Wheel Control")
        
        # Telemetry Tab
        self.telemetry_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.telemetry_tab, text="Telemetry")
        
        # Setup tabs
        self.setup_sensor_tab()
        self.setup_reaction_wheel_tab()
        self.setup_telemetry_tab()
        
        # Start update thread
        self.update_thread = threading.Thread(target=self.update_ui)
        self.update_thread.daemon = True
        self.update_thread.start()
    
    def setup_sensor_tab(self):
        """Create visualizations for sensor data"""
        # IMU Data Plot
        self.fig_imu, (self.ax_accel, self.ax_gyro) = plt.subplots(2, 1, figsize=(10, 6))
        self.canvas_imu = FigureCanvasTkAgg(self.fig_imu, master=self.sensor_tab)
        self.canvas_imu.get_tk_widget().pack()
    
    def setup_reaction_wheel_tab(self):
        """Controls for reaction wheel system"""
        # Stabilization Mode Toggle
        self.stabilization_var = tk.BooleanVar(value=False)
        stabilization_check = ttk.Checkbutton(
            self.reaction_wheel_tab, 
            text="Stabilization Mode", 
            variable=self.stabilization_var,
            command=self.toggle_stabilization
        )
        stabilization_check.pack()
        
        # Manual Motor Speed Sliders
        self.motor_sliders = []
        for i in range(3):
            slider_frame = ttk.Frame(self.reaction_wheel_tab)
            slider_frame.pack(fill='x', padx=10, pady=5)
            
            ttk.Label(slider_frame, text=f"Motor {i+1} Speed:").pack(side='left')
            slider = ttk.Scale(
                slider_frame, 
                from_=-100, to=100, 
                orient='horizontal', 
                length=300
            )
            slider.pack(side='left', expand=True, fill='x')
            self.motor_sliders.append(slider)
    
    def setup_telemetry_tab(self):
        """Display system telemetry and logs"""
        self.telemetry_text = tk.Text(self.telemetry_tab, height=30, width=80)
        self.telemetry_text.pack()
    
    def update_ui(self):
        """Continuously update UI elements"""
        while True:
            # Update sensor plots
            self.update_sensor_plots()
            
            # Update telemetry log
            self.update_telemetry()
            
            time.sleep(0.1)  # 10 Hz update
    
    def update_sensor_plots(self):
        """Update matplotlib plots with latest sensor data"""
        sensor_data = self.flight_computer.sensor_data
        
        # Update acceleration plot
        self.ax_accel.clear()
        self.ax_accel.plot(sensor_data['imu']['accel'], label='Acceleration')
        self.ax_accel.set_title('Acceleration')
        
        # Update gyroscope plot
        self.ax_gyro.clear()
        self.ax_gyro.plot(sensor_data['imu']['gyro'], label='Gyroscope')
        self.ax_gyro.set_title('Gyroscope')
        
        self.canvas_imu.draw()
    
    def toggle_stabilization(self):
        """Enable/disable stabilization mode"""
        self.flight_computer.reaction_wheel_state['stabilization_mode'] = \
            self.stabilization_var.get()
    
    def update_telemetry(self):
        """Update telemetry log display"""
        telemetry_log = f"""
        System Status: Active
        Pressure: {self.flight_computer.sensor_data['pressure']} hPa
        Temperature: {self.flight_computer.sensor_data['temperature']} °C
        Current Orientation: {self.flight_computer.reaction_wheel_state['current_orientation']}
        Stabilization Mode: {self.flight_computer.reaction_wheel_state['stabilization_mode']}
        """
        self.telemetry_text.delete(1.0, tk.END)
        self.telemetry_text.insert(tk.END, telemetry_log)
    
    def run(self):
        self.root.mainloop()

def main():
    flight_computer = FlightComputer()  # From main script
    ui = FlightComputerUI(flight_computer)
    ui.run()

if __name__ == "__main__":
    main()
