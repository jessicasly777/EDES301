# test_blynk.py
import blynklib
from DONTSHAREconfig import BLYNK_AUTH_TOKEN

blynk = blynklib.Blynk(BLYNK_AUTH_TOKEN)

print("Connecting...")
for i in range(50):
    blynk.run()

print("Check isHardwareConnected in browser NOW while this is running")
input("Press Enter when done...")