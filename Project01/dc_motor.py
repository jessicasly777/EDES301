# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------
# DC Motor Driver
# --------------------------------------------------------------------------
# License:
# Copyright 2026 - Jessica Shi
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
# may be used to endorse or promote products derived from this software without
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND WITHOUT ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
# THE POSSIBILITY OF SUCH DAMAGE.
# --------------------------------------------------------------------------
#
# DC Motor Driver
#
#   This driver controls a single DC motor via a DRV8833 dual H-bridge
#   motor driver board. Each motor requires two pins connected to the
#   driver board IN pins.
#
#   The DRV8833 controls both speed and direction through the IN pins:
#     - IN1 (PWM pin) : controls motor speed via duty cycle (0-100%)
#     - IN2 (GPIO pin): controls motor direction (HIGH or LOW)
#
#   Motor layout (4WD):
#     Motor A (Front Left)  : IN1=P1_36, IN2=P2_17
#     Motor B (Front Right) : IN1=P1_33, IN2=P2_19
#     Motor C (Rear Left)   : IN1=P2_01, IN2=P2_27
#     Motor D (Rear Right)  : IN1=P2_03, IN2=P2_29
#
#   DRV8833 Board connections:
#     VCC  : 5V from step down module
#     GND  : shared ground with PocketBeagle and battery
#     SLEEP: leave disconnected (pulled high internally)
#     ULT  : leave disconnected
#
# --------------------------------------------------------------------------
#
# Software API:
#
#   DCMotor(in1_pin, in2_pin)
#     - in1_pin : PWM capable pin for speed control
#                 Must be a PWM pin (e.g. "P1_36", "P1_33", "P2_01", "P2_03")
#     - in2_pin : GPIO pin for direction control
#                 (e.g. "P2_17", "P2_19", "P2_27", "P2_29")
#
#     forward(speed)
#       - Drive motor forward at given speed (0-100)
#
#     backward(speed)
#       - Drive motor backward at given speed (0-100)
#
#     stop()
#       - Stop the motor immediately
#
#     cleanup()
#       - Release PWM and GPIO pins safely on shutdown
#
# --------------------------------------------------------------------------

import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.GPIO as GPIO

class DCMotor:
    def __init__(self, in1_pin, in2_pin):
        """
        in1_pin : PWM capable pin for speed control (e.g. "P1_36")
        in2_pin : GPIO pin for direction control    (e.g. "P2_17")
        """
        self.in1_pin = in1_pin
        self.in2_pin = in2_pin

        # Set up IN2 as GPIO output for direction control
        GPIO.setup(self.in2_pin, GPIO.OUT)
        GPIO.output(self.in2_pin, GPIO.LOW)

        # Set up IN1 as PWM for speed control
        # Starts at 0% duty cycle (stopped)
        PWM.start(self.in1_pin, 0, 50)

        print("DCMotor initialized on IN1={}, IN2={}".format(in1_pin, in2_pin))

    def forward(self, speed):
        """
        Drive motor forward.
        speed: integer 0-100 (percentage of max speed)
        """
        speed = max(0, min(100, speed))
        GPIO.output(self.in2_pin, GPIO.LOW)
        PWM.set_duty_cycle(self.in1_pin, speed)
        print("Motor FORWARD at {}% speed".format(speed))

    def backward(self, speed):
        """
        Drive motor backward.
        speed: integer 0-100 (percentage of max speed)
        """
        speed = max(0, min(100, speed))
        GPIO.output(self.in2_pin, GPIO.HIGH)
        PWM.set_duty_cycle(self.in1_pin, 100 - speed)
        print("Motor BACKWARD at {}% speed".format(speed))

    def stop(self):
        """
        Stop the motor immediately.
        """
        GPIO.output(self.in2_pin, GPIO.LOW)
        PWM.set_duty_cycle(self.in1_pin, 0)
        print("Motor STOPPED")

    def cleanup(self):
        """
        Release PWM and GPIO pins safely on shutdown.
        Always call this when shutting down.
        """
        self.stop()
        PWM.stop(self.in1_pin)
        print("DCMotor cleaned up")
