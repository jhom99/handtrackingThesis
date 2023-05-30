/*
 * @author Julian Hom
 * recieve Data from Unity and display haptic user feedback with haptic driver
 * based on recieved Data
 */
#include <Wire.h>
#include "Haptic_Driver.h"

// Create an instance of the Haptic_Driver class with the name "indexDrive"
Haptic_Driver indexDrive;

// Setup function - runs once at the start of the program
void setup() {
  
  // Start the serial communication
  Serial.begin(9600);
  
  // Start the I2C communication
  Wire.begin();
  
  // Attempt to initialize communication with the Haptic Driver
  if (!indexDrive.begin()) {
    Serial.println("Could not communicate with Haptic Driver.");
  }
  else {
    Serial.println("Qwiic Haptic Driver DA7280 found!");
  }

  // Attempt to set default motor settings
  if (!indexDrive.defaultMotor()) {
    Serial.println("Could not set default settings.");
  }
  
  // Disable frequency tracking
  indexDrive.enableFreqTrack(false);

  // Set the I2C operation mode to DRO_MODE
  indexDrive.setOperationMode(DRO_MODE);

  // Wait for 1 second
  delay(1000);
}

// Function to stop the vibration of the index motor
void stopIndex() {
  indexDrive.setVibrate(0);
}

// Function to vibrate the index motor
void indexVibrate() {
  indexDrive.setVibrate(127);
}

void loop() {

  // Check if there is serial data available
  if (Serial.available() > 0) {
    
    // Read the incoming character
    char c = Serial.read();
    
    // If the character is '1', start vibrating the index motor
    if (c == '1') {
      indexVibrate();
    } 
    // If the character is '0', stop vibrating the index motor
    else if (c == '0') {
      stopIndex();
    }
  }
}
