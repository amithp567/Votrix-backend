import serial
import adafruit_fingerprint

uart = serial.Serial("/dev/ttyUSB0", baudrate=57600, timeout=1)
finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

if finger.empty_library() == adafruit_fingerprint.OK:
    print("Sensor wiped successfully! All 127 slots are now empty.")