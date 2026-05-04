# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------
# Communication Driver
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
# Communication Driver
#
#   This driver handles wireless communication between the Blynk mobile
#   app joystick and the PocketBeagle. It reads joystick X and Y axis
#   values from Blynk virtual pins and converts them into simple
#   directional commands with a numerical speed value.
#
#   Virtual Pin Mapping:
#     V0 - Joystick X axis (left/right) : -100 to 100
#     V1 - Joystick Y axis (forward/back): -100 to 100
#
#   Commands produced:
#     "F" - Forward   (Y > threshold)
#     "B" - Backward  (Y < -threshold)
#     "L" - Left      (X < -threshold)
#     "R" - Right     (X > threshold)
#     "E" - Emergency stop (all values near zero)
#
# --------------------------------------------------------------------------
#
# Software API:
#
#   Communication()
#     - Connects to Blynk cloud using credentials from config.py
#
#     get_command()
#       - Returns a tuple (command, value)
#       - command : str one of "F", "B", "L", "R", "E"
#       - value   : int 0-100 representing speed/intensity
#
#     start()
#       - Call once before the main loop
#
#     run()
#       - Call every loop iteration to poll Blynk for new joystick values
#
#     stop()
#       - Call on shutdown to reset command state
#
# --------------------------------------------------------------------------

import requests
import time
from DONTSHAREconfig import BLYNK_AUTH_TOKEN

DEAD_ZONE = 10

class Communication:
    def __init__(self):
        self.x_value = 0
        self.y_value = 0
        self.command = "E"
        self.speed   = 0
        self.server  = "https://blynk.cloud/external/api"
        print("Communication initialized")

    def _get_pin(self, pin):
        """Get value from Blynk virtual pin via HTTP REST API."""
        try:
            # FIX: correct Blynk IoT API URL format is &pin=V0, not &v=0
            url = "{}/get?token={}&pin=V{}".format(
                self.server, BLYNK_AUTH_TOKEN, pin)
            response = requests.get(url, timeout=2)
            print("[PIN V{}] status={} body={}".format(
                pin, response.status_code, response.text))
            if response.status_code == 200:
                return int(float(response.text.strip('[]"')))
        except Exception as e:
            print("[PIN V{}] ERROR: {}".format(pin, e))
        return 0

    def _update_command(self):
        x = self.x_value
        y = self.y_value

        if y > DEAD_ZONE:
            self.command = "F"
            self.speed   = y
        elif y < -DEAD_ZONE:
            self.command = "B"
            self.speed   = abs(y)
        elif x > DEAD_ZONE:
            self.command = "R"
            self.speed   = x
        elif x < -DEAD_ZONE:
            self.command = "L"
            self.speed   = abs(x)
        else:
            self.command = "E"
            self.speed   = 0

        print("[Command] {} at speed {}".format(self.command, self.speed))

    def get_command(self):
        return (self.command, self.speed)

    def start(self):
        print("Communication started — joystick ready")

    def run(self):
        """Poll Blynk for joystick values via HTTP REST API."""
        self.x_value = self._get_pin(0)
        self.y_value = self._get_pin(1)
        self._update_command()

    def stop(self):
        self.command = "E"
        self.speed   = 0
        print("Communication stopped")
