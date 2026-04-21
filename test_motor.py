# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------
# Motor Test Driver
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
# Motor Test
#
#   Standalone test file to verify motor wiring and DCMotor class
#   are working correctly before running the full RC car.
#
#   Tests each motor individually:
#     - Forward for 3 seconds
#     - Stop for 1 second
#     - Backward for 3 seconds
#     - Stop for 1 second
#
#   Without battery: print statements only, no spinning
#   With battery:    motors spin one at a time
#
#   If a motor spins the wrong direction, swap its OUT1/OUT2
#   wires on the DRV8833 board — no code change needed!
#
#   Pin assignments match main.py and wiring diagram:
#     Motor A (Front Left)  : IN1=P1_36, IN2=P2_17
#     Motor B (Front Right) : IN1=P1_33, IN2=P2_19
#     Motor C (Rear Left)   : IN1=P2_01, IN2=P2_27
#     Motor D (Rear Right)  : IN1=P2_03, IN2=P2_29
#
# --------------------------------------------------------------------------

from dc_motor import DCMotor
import time

def test_motor(name, motor, speed=50):
    """
    Test a single motor — forward, stop, backward, stop.
    name  : string label e.g. "Motor A (Front Left)"
    motor : DCMotor object
    speed : test speed 0-100 (default 50%)
    """
    print("----------------------------------")
    print("Testing: {}".format(name))
    print("----------------------------------")

    print("Forward at {}%...".format(speed))
    motor.forward(speed)
    time.sleep(3)

    print("Stopping...")
    motor.stop()
    time.sleep(1)

    print("Backward at {}%...".format(speed))
    motor.backward(speed)
    time.sleep(3)

    print("Stopping...")
    motor.stop()
    time.sleep(1)

    print("{} test complete!".format(name))
    print("")

# ------------------------------------------------------------------
# Pin assignments — must match main.py
# ------------------------------------------------------------------

# Motor A — Front Left
FL_PINS = ("P2_1", "P2_27")
# Motor B — Front Right
FR_PINS = ("P1_36", "P2_17")
# Motor C — Rear Left 
RL_PINS = ("P1_33", "P2_19")
# Motor D — Rear Right
RD_PINS = ("P2_3", "P2_29")

# ------------------------------------------------------------------
# Create motor objects
# ------------------------------------------------------------------

print("Initializing motors...")
motor_a = DCMotor(*FL_PINS)
motor_b = DCMotor(*FR_PINS)
motor_c = DCMotor(*RL_PINS)
motor_d = DCMotor(*RD_PINS)
print("All motors initialized!")
print("")

# ------------------------------------------------------------------
# Run tests
# ------------------------------------------------------------------

try:
    # Test one motor at a time
    test_motor("Motor A - Front Left",  motor_a)
    test_motor("Motor B - Front Right", motor_b)
    test_motor("Motor C - Rear Left",   motor_c)
    test_motor("Motor D - Rear Right",  motor_d)

    print("==================================")
    print("All motor tests complete!")
    print("If all motors spun correctly,")
    print("you are ready to run main.py!")
    print("==================================")

except KeyboardInterrupt:
    print("Test stopped by user")

finally:
    # Always cleanup on exit
    print("Cleaning up...")
    motor_a.cleanup()
    motor_b.cleanup()
    motor_c.cleanup()
    motor_d.cleanup()
    print("Done!")