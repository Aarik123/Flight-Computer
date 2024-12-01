# DIY Advanced Flight Computer System

## Project Overview

This open-source flight computer project is designed for amateur rocketry and drone enthusiasts, providing a robust, modular solution for flight stabilization and data acquisition. The system combines cutting-edge sensor technology, advanced control algorithms, and a user-friendly interface to deliver precise orientation control and comprehensive telemetry.

### Key Features

- **Advanced Sensor Integration**: Utilizes Arduino Nano 33 BLE Sense's high-precision sensors
- **Reaction Wheel Stabilization**: Three-axis attitude control using DC motor-driven reaction wheels
- **Real-time Data Monitoring**: Comprehensive UI for tracking flight parameters
- **Flexible Architecture**: Suitable for both amateur rocketry and drone applications

## System Architecture

### Hardware Components

1. **Main Controller**: Raspberry Pi 4 / 2W
   - Central processing unit
   - Runs flight control software
   - Manages high-level system logic

2. **Sensor Hub**: Arduino Nano 33 BLE Sense
   - Dedicated sensor data acquisition
   - Provides real-time IMU, pressure, and environmental data
   - Acts as communication bridge

3. **Actuation System**: L298N Motor Driver with 3x 130 DC Motors
   - Implements reaction wheel stabilization
   - Enables precise 3-axis orientation control

### Software Components

- **Python Flight Computer Script**:
  - Multi-threaded sensor and motor control
  - PID-based stabilization algorithms
  - Comprehensive logging system

- **Arduino Sensor Hub Firmware**:
  - Sensor data acquisition
  - Motor control interface
  - JSON-based communication protocol

- **Cross-Platform Tkinter UI**:
  - Real-time sensor visualization
  - Manual and automated control modes
  - Telemetry monitoring

## Installation & Setup

### Prerequisites

- Raspberry Pi 4 or 2W (64-bit OS recommended)
- Arduino Nano 33 BLE Sense
- L298N Motor Driver
- 3x 130 DC Motors
- Python 3.8+
- Arduino IDE

### Dependencies

- Python Libraries:
  - numpy
  - matplotlib
  - pyserial
  - scipy
  - tkinter

- Arduino Libraries:
  - Arduino_LSM9DS1
  - Arduino_LPS22HB
  - Arduino_HTS221
  - ArduinoJson
  - L298N

### Wiring Diagram

[Placeholder for detailed wiring diagram showing connections between Raspberry Pi, Arduino, and L298N Motor Driver]

## Calibration & Configuration

1. Sensor Calibration
2. PID Parameter Tuning
3. Motor Alignment

## Safety Considerations

⚠️ **Important Safety Notes**:
- Always perform initial tests in a controlled environment
- Use appropriate protective gear
- Comply with local regulations regarding amateur rocketry and drone operations

## Contributing

Contributions are welcome! Please read our [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

- Arduino Community
- Raspberry Pi Foundation
- Open-source sensor and control libraries

## Future Roadmap

- GPS Integration
- Machine Learning-based Trajectory Prediction
- Enhanced Sensor Fusion Algorithms
- Wireless Telemetry Module

## Disclaimer

This project is for educational and experimental purposes. Users should exercise extreme caution and adhere to all relevant safety guidelines and legal requirements.
