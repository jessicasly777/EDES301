# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------
# Limit Switch Driver
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
# Limit Switch Driver
#
#   This driver provides a limit switch / emergency stop button that runs
#   in its own execution thread, based on the ThreadedButton pattern.
#
#   The switch monitors a single GPIO pin on the PocketBeagle. When pressed,
#   it immediately triggers an emergency stop callback to halt all motors
#   regardless of what the main loop is doing.
#
#   This driver supports both pull up and pull down resistor configurations:
#     - active_low=True  : pull up resistor (pin HIGH when unpressed,
#                          LOW when pressed) — default
#     - active_low=False : pull down resistor (pin LOW when unpressed,
#                          HIGH when pressed)
#
# --------------------------------------------------------------------------
#
# Software API:
#
#   LimitSwitch(pin, sleep_time=0.1, active_low=True)
#     - pin        : PocketBeagle GPIO pin name (e.g. "P9_15")
#     - sleep_time : time in seconds between checks (default 0.1)
#     - active_low : True for pull up config, False for pull down
#
#     start()
#       - Starts the switch monitoring thread
#
#     is_pressed()
#       - Returns True if switch is currently pressed, False otherwise
#
#     set_callback(function)
#       - Set the function to call when switch is pressed
#       - Used to trigger emergency stop on the RC car
#
#     cleanup()
#       - Stops the thread safely on shutdown
#
# --------------------------------------------------------------------------

import Adafruit_BBIO.GPIO as GPIO
import threading
import time

class LimitSwitch:
    def __init__(self, pin, sleep_time=0.02, active_low=True):
        self.pin = pin
        self.sleep_time = sleep_time
        self.active_low = active_low
        self._callback = None
        self._running = False
        self._thread = None

        # If your BBIO version supports this, use internal pull-up
        try:
            if self.active_low:
                GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            else:
                GPIO.setup(self.pin, GPIO.IN)
        except TypeError:
            GPIO.setup(self.pin, GPIO.IN)

        print(f"LimitSwitch initialized on pin={pin}, active_low={active_low}")

    def _is_physically_pressed(self):
        pin_value = GPIO.input(self.pin)
        if self.active_low:
            return pin_value == GPIO.LOW
        else:
            return pin_value == GPIO.HIGH

    def _monitor(self):
        print("LimitSwitch thread started — monitoring for press...")
        was_pressed = False

        while self._running:
            pressed = self._is_physically_pressed()
            
            if pressed and not was_pressed:
                print("EMERGENCY STOP — limit switch pressed!")
                if self._callback is not None:
                    self._callback()
                time.sleep(0.05)   # debounce

            was_pressed = pressed
            time.sleep(self.sleep_time)

    def set_callback(self, function):
        self._callback = function
        print("LimitSwitch callback set")

    def is_pressed(self):
        return self._is_physically_pressed()

    def start(self):
        if not self._running:
            self._running = True
            self._thread = threading.Thread(target=self._monitor, daemon=True)
            self._thread.start()
            print("LimitSwitch thread running")

    def cleanup(self):
        self._running = False
        if self._thread is not None:
            self._thread.join(timeout=0.2)
        print("LimitSwitch cleaned up")
