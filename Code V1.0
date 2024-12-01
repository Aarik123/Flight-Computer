#include <Arduino_LSM9DS1.h>
#include <Arduino_LPS22HB.h>
#include <Arduino_HTS221.h>
#include <ArduinoJson.h>
#include <L298N.h>

// Pin definitions for L298N Motor Driver
#define ENA 9
#define IN1 10
#define IN2 11
#define ENB 6
#define IN3 7
#define IN4 8
#define ENC 5
#define IN5 4
#define IN6 3

// Create motor objects
L298N motor1(ENA, IN1, IN2);
L298N motor2(ENB, IN3, IN4);
L298N motor3(ENC, IN5, IN6);

// JSON serialization buffer
StaticJsonDocument<200> jsonBuffer;

void setup() {
    Serial.begin(115200);
    
    // Initialize IMU
    if (!IMU.begin()) {
        Serial.println("Failed to initialize IMU!");
        while (1);
    }
    
    // Initialize Pressure Sensor
    if (!BARO.begin()) {
        Serial.println("Failed to initialize Pressure Sensor!");
        while (1);
    }
    
    // Initialize Temperature & Humidity Sensor
    if (!HTS.begin()) {
        Serial.println("Failed to initialize Temp/Humidity Sensor!");
        while (1);
    }
    
    // Configure motor control pins
    motor1.setSpeed(0);
    motor2.setSpeed(0);
    motor3.setSpeed(0);
}

void loop() {
    float accelX, accelY, accelZ;
    float gyroX, gyroY, gyroZ;
    float pressure, temperature;
    
    // Read IMU data
    if (IMU.accelerationAvailable() && IMU.gyroscopeAvailable()) {
        IMU.readAcceleration(accelX, accelY, accelZ);
        IMU.readGyroscope(gyroX, gyroY, gyroZ);
        
        // Read environmental data
        pressure = BARO.readPressure();
        temperature = HTS.readTemperature();
        
        // Prepare JSON packet
        jsonBuffer.clear();
        JsonObject sensorData = jsonBuffer.createNestedObject();
        
        // IMU data
        JsonObject imu = sensorData.createNestedObject("imu");
        JsonArray accel = imu.createNestedArray("accel");
        accel.add(accelX);
        accel.add(accelY);
        accel.add(accelZ);
        
        JsonArray gyro = imu.createNestedArray("gyro");
        gyro.add(gyroX);
        gyro.add(gyroY);
        gyro.add(gyroZ);
        
        // Environmental data
        sensorData["pressure"] = pressure;
        sensorData["temperature"] = temperature;
        
        // Serialize and send data
        serializeJson(sensorData, Serial);
        Serial.println();
    }
    
    // Check for motor control commands
    if (Serial.available()) {
        String motorCommand = Serial.readStringUntil('\n');
        deserializeJson(jsonBuffer, motorCommand);
        JsonObject motorSpeeds = jsonBuffer.as<JsonObject>();
        
        // Set motor speeds
        motor1.setSpeed(motorSpeeds["motor1"]);
        motor2.setSpeed(motorSpeeds["motor2"]);
        motor3.setSpeed(motorSpeeds["motor3"]);
    }
    
    delay(50);  // 20 Hz update rate
}
