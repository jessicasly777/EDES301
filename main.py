# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------
# RC Car Main Entry Point
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
# RC Car Main Entry Point
#
#   This is the only file you run to start the RC car.
#   It defines the pin assignments for all motors and the limit switch,
#   creates the RCCar object, and starts the main loop.
#
#   Pin assignments — fill these in once your wiring is confirmed:
#
#   Each motor needs 3 pins: (pwm_pin, in1_pin, in2_pin)
#
#   Motor layout viewed from above:
#
#         FRONT
#     FL       FR
#     RL       RR
#         REAR
#
# --------------------------------------------------------------------------

from rc_car import RCCar

# ------------------------------------------------------------------
# Pin assignments
# Update these to match your actual wiring on the PocketBeagle
# ------------------------------------------------------------------

# Front left motor A  (in1_pwm, in2_gpio)
FL_PINS = ("P1_36", "P2_17")

# Front right motor B (in1_pwm, in2_gpio)
FR_PINS = ("P1_33", "P2_19")

# Rear left motor C   (in1_pwm, in2_gpio)
RL_PINS = ("P2_1", "P2_27")

# Rear right motor D  (in1_pwm, in2_gpio)
RR_PINS = ("P2_3", "P2_29")


# Limit switch
SWITCH_PIN = "P1_31"




if __name__ == "__main__":
    car = RCCar(
        fl_pins    = FL_PINS,
        fr_pins    = FR_PINS,
        rl_pins    = RL_PINS,
        rr_pins    = RR_PINS,
        switch_pin = SWITCH_PIN
    )

    car.run()
    
#restore
#sudo pfctl -e
#sudo sysctl -w net.inet.ip.forwarding=0