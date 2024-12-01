import os
import time
import serial
import threading
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter
import pygame
import tkinter as tk
from tkinter import ttk
import json
import logging

# Logging configuration
logging.basicConfig(filename='/home/pi/flight_computer/flight_log.txt', 
                    level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s: %(message)s')

class FlightComputer:
    def __init__(self):
        # Serial communication with Arduino sensor hub
        self.arduino_port = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
        
        # Sensor data storage
        self.sensor_data = {
            'imu': {'accel': [0, 0, 0], 'gyro': [0, 0, 0]},
            'pressure': 0,
            'temperature': 0,
            'gps': {'lat': 0, 'lon': 0, 'alt': 0}
        }
        
        # Reaction wheel control parameters
        self.reaction_wheel_state = {
            'motor_speeds': [0, 0, 0],
            'stabilization_mode': False,
            'current_orientation': [0, 0, 0]
        }
        
        # Control threads
        self.sensor_thread = threading.Thread(target=self.read_sensor_data)
        self.reaction_wheel_thread = threading.Thread(target=self.control_reaction_wheels)
        
        # Logging
        logging.info("Flight Computer Initialized")
    
    def read_sensor_data(self):
        """
        Continuously read sensor data from Arduino sensor hub
        Uses JSON-formatted serial communication
        """
        while True:
            try:
                # Read JSON-formatted sensor data
                raw_data = self.arduino_port.readline().decode('utf-8').strip()
                sensor_packet = json.loads(raw_data)
                
                # Update sensor data dictionary
                self.sensor_data.update(sensor_packet)
                
                # Log critical sensor information
                logging.info(f"Sensor Data: {sensor_packet}")
                
                time.sleep(0.1)  # 10 Hz sampling rate
            except Exception as e:
                logging.error(f"Sensor Read Error: {e}")
                time.sleep(1)
    
    def control_reaction_wheels(self):
        """
        Implement PID-based stabilization for reaction wheels
        """
        # PID control constants
        Kp = 0.5  # Proportional gain
        Ki = 0.1  # Integral gain
        Kd = 0.01  # Derivative gain
        
        # Error tracking
        prev_error = [0, 0, 0]
        integral_error = [0, 0, 0]
        
        while self.reaction_wheel_state['stabilization_mode']:
            current_orientation = self.sensor_data['imu']['gyro']
            target_orientation = [0, 0, 0]  # Level orientation
            
            # Calculate error
            error = [target - current for target, current in zip(target_orientation, current_orientation)]
            
            # PID calculations
            integral_error = [ie + e for ie, e in zip(integral_error, error)]
            derivative_error = [e - pe for e, pe in zip(error, prev_error)]
            
            # Calculate motor outputs
            motor_outputs = [
                Kp * e + Ki * ie + Kd * de 
                for e, ie, de in zip(error, integral_error, derivative_error)
            ]
            
            # Send motor control signals
            self.send_motor_commands(motor_outputs)
            
            prev_error = error
            time.sleep(0.05)  # 20 Hz update rate
    
    def send_motor_commands(self, motor_speeds):
        """
        Send motor speed commands to L298N motor driver
        """
        try:
            # Convert to appropriate motor driver protocol
            motor_packet = json.dumps({
                'motor1': motor_speeds[0],
                'motor2': motor_speeds[1],
                'motor3': motor_speeds[2]
            })
            self.arduino_port.write(motor_packet.encode('utf-8'))
        except Exception as e:
            logging.error(f"Motor Control Error: {e}")
    
    def start(self):
        """
        Start all flight computer threads
        """
        self.sensor_thread.start()
        self.reaction_wheel_thread.start()

def main():
    flight_computer = FlightComputer()
    flight_computer.start()

if __name__ == "__main__":
    main()
