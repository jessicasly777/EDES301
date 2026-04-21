# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------
# RC Car Driver
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
# RC Car Driver
#
#   This class creats and manages the DCMotor, Communication, and LimitSwitch objects and contains
#   the main run loop that ties everything together.
#
#   The car uses a tank turn style steering:
#     Forward  : all motors drive forward at given speed
#     Backward : all motors drive backward at given speed
#     Left     : left motors backward, right motors forward
#     Right    : left motors forward, right motors backward
#     Stop     : all motors stop immediately
#
#   The limit switch runs in its own thread and triggers an emergency
#   stop instantly regardless of what the main loop is doing.
#
#   Motor layout (4WD):
#     front_left  / front_right  — front two motors
#     rear_left   / rear_right   — rear two motors
#
# --------------------------------------------------------------------------
#
# Software API:
#
#   RCCar(fl_pins, fr_pins, rl_pins, rr_pins, switch_pin)
#     - fl_pins    : tuple (pwm, in1, in2) for front left motor
#     - fr_pins    : tuple (pwm, in1, in2) for front right motor
#     - rl_pins    : tuple (pwm, in1, in2) for rear left motor
#     - rr_pins    : tuple (pwm, in1, in2) for rear right motor
#     - switch_pin : GPIO pin for limit switch / emergency button
#
#     run()
#       - Starts the main loop — call this to start the car
#       - Runs until keyboard interrupt (Ctrl+C) or emergency stop
#
#     stop()
#       - Stops all motors immediately
#
#     cleanup()
#       - Safely shuts down all motors, comms and switch on exit
#
# --------------------------------------------------------------------------

from dc_motor      import DCMotor
from communication import Communication
from limit_switch  import LimitSwitch
import time

class RCCar:
    def __init__(self, fl_pins, fr_pins, rl_pins, rr_pins, switch_pin):

        print("Initializing RC Car...")

        # --- Create 4 motors ---
        # Each motor takes (pwm_pin, in1_pin, in2_pin)
        self.front_left  = DCMotor(*fl_pins)
        self.front_right = DCMotor(*fr_pins)
        self.rear_left   = DCMotor(*rl_pins)
        self.rear_right  = DCMotor(*rr_pins)

        # --- Create communication (Blynk joystick) ---
        self.comm = Communication()

        # --- Create limit switch ---
        self.switch = LimitSwitch(switch_pin, active_low=True)
        # Connect emergency stop to the switch
        # When switch is pressed, _emergency_stop() is called automatically
        self.switch.set_callback(self._emergency_stop)

        # Flag to control the main loop
        self._running = False

        print("RC Car ready!")

    # ------------------------------------------------------------------
    # Motor command methods
    # ------------------------------------------------------------------

    def _forward(self, speed):
        """All four motors drive forward."""
        self.front_left.forward(speed)
        self.front_right.forward(speed)
        self.rear_left.forward(speed)
        self.rear_right.forward(speed)
        print(f"CAR: Forward at {speed}%")

    def _backward(self, speed):
        """All four motors drive backward."""
        self.front_left.backward(speed)
        self.front_right.backward(speed)
        self.rear_left.backward(speed)
        self.rear_right.backward(speed)
        print(f"CAR: Backward at {speed}%")

    def _turn_left(self, speed):
        """
        Tank turn left:
        Left motors go backward, right motors go forward.
        Car spins left on the spot.
        """
        self.front_left.backward(speed)
        self.rear_left.backward(speed)
        self.front_right.forward(speed)
        self.rear_right.forward(speed)
        print(f"CAR: Tank turn LEFT at {speed}%")

    def _turn_right(self, speed):
        """
        Tank turn right:
        Left motors go forward, right motors go backward.
        Car spins right on the spot.
        """
        self.front_left.forward(speed)
        self.rear_left.forward(speed)
        self.front_right.backward(speed)
        self.rear_right.backward(speed)
        print(f"CAR: Tank turn RIGHT at {speed}%")

    def stop(self):
        """Stop all four motors immediately."""
        self.front_left.stop()
        self.front_right.stop()
        self.rear_left.stop()
        self.rear_right.stop()
        print("CAR: All motors stopped")

    def _emergency_stop(self):
        """
        Called automatically by the limit switch thread when
        the emergency button is pressed. Stops everything immediately.
        """
        print("!!! EMERGENCY STOP TRIGGERED !!!")
        self.stop()
        self._running = False  # exits the main run loop

    # ------------------------------------------------------------------
    # Main run loop
    # ------------------------------------------------------------------

    def run(self):
        """
        Main loop — reads joystick commands from Communication
        and sends them to the motors.
        Runs until Ctrl+C or emergency stop is triggered.
        """
        print("Starting RC Car main loop — press Ctrl+C to stop")

        # Start the limit switch thread
        self.switch.start()

        # Start Blynk communication
        self.comm.start()

        self._running = True

        try:
            while self._running:
                # Keep Blynk connection alive and process incoming data
                self.comm.run()

                # Get the latest command from the joystick
                command, speed = self.comm.get_command()

                # Match command to motor action
                if command == "F":
                    self._forward(speed)

                elif command == "B":
                    self._backward(speed)

                elif command == "L":
                    self._turn_left(speed)

                elif command == "R":
                    self._turn_right(speed)

                elif command == "E":
                    self.stop()

                # Small delay to prevent overloading the PocketBeagle
                time.sleep(0.05)

        except KeyboardInterrupt:
            # Ctrl+C pressed — exit cleanly
            print("Keyboard interrupt — shutting down...")

        finally:
            # Always clean up even if something crashes
            self.cleanup()

    # ------------------------------------------------------------------
    # Cleanup
    # ------------------------------------------------------------------

    def cleanup(self):
        """
        Safely shuts down all components.
        Always called on exit whether normal or crash.
        """
        print("Cleaning up RC Car...")
        self.stop()
        self.comm.stop()
        self.switch.cleanup()
        self.front_left.cleanup()
        self.front_right.cleanup()
        self.rear_left.cleanup()
        self.rear_right.cleanup()
        print("RC Car shutdown complete")