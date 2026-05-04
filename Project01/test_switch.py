# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------
# Limit Switch Test
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
# Limit Switch Test
#
#   Standalone test file to verify the limit switch wiring and
#   LimitSwitch class are working correctly before connecting motors.
#
#   Expected behavior:
#     - Terminal prints "Switch test running" on start
#     - Press button → prints "Button pressed! Emergency stop would trigger"
#     - Hold button → prints "Switch is currently held down..."
#     - Release button → returns to waiting silently
#     - Ctrl+C → prints "Test stopped" and exits cleanly
#
# --------------------------------------------------------------------------


from limit_switch import LimitSwitch
import time

def my_test_callback():
    print(">>> Button pressed! Emergency stop would trigger here")

# Use the same pin as defined in main.py
switch = LimitSwitch("P1_31", active_low=True)
switch.set_callback(my_test_callback)
switch.start()

print("----------------------------------")
print("Limit switch test running!")
print("Press your button to test...")
print("Press Ctrl+C to stop")
print("----------------------------------")

try:
    while True:
        if switch.is_pressed():
            print("Switch is currently held down...")
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Test stopped")
    switch.cleanup()
    
    
