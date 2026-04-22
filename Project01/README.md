Main control flow of this project Blynk App (Joystick) ↓ communication.py ↓ main.py (control logic) ↓ dc_motor.py ↓ DRV8833 → Motors

communication.py: Handles all communication between the PocketBeagle and the Blynk mobile application. It connects to the Blynk cloud and reads joystick input from two virtual pins:

V0 for left/right (X-axis) V1 for forward/backward (Y-axis)

dc_motor.py: Cntrols the DC motors through the DRV8833 motor driver. Each motor is controlled using two pins:

A PWM pin for speed control A GPIO pin for direction

The module provides simple methods:

forward(speed) backward(speed) stop() cleanup()

limit_switch.py: This module implements an emergency stop mechanism using a physical limit switch.

pin.sh: Cnfigures the PocketBeagle pins before running the system.

main.py: Initializes all components, including the communication module, motor drivers, and limit switch. It then runs a continuous loop that:

test_motor.py: This file is used to test each motor individually. It runs a sequence where each motor moves forward, stops, moves backward, and stops again. This helps verify that wiring and control logic are correct before running the full system. If a motor spins in the wrong direction, the wires on the motor driver should be swapped rather than modifying the code.

test_blynk.py: Tests the connection to the Blynk cloud. It confirms that the PocketBeagle can establish a connection and communicate with the app. This is useful for debugging network issues independently from the rest of the system.
