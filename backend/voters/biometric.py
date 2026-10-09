import serial
import time
import adafruit_fingerprint


uart = serial.Serial("/dev/ttyUSB0", baudrate=57600, timeout=1)
finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

if finger.read_sysparam() != adafruit_fingerprint.OK:
    raise RuntimeError("Fingerprint sensor not detected")

print("Fingerprint sensor ready")


def wait_for_finger(timeout=10):
    start = time.time()
    while finger.get_image() != adafruit_fingerprint.OK:
        if time.time() - start > timeout:
            return False
    return True


def wait_for_removal(timeout=10):
    start = time.time()
    while finger.get_image() != adafruit_fingerprint.NOFINGER:
        if time.time() - start > timeout:
            return False
    return True


def enroll_fingerprint():
    print("\nStarting fingerprint enrollment...")

    print("Place finger...")
    if not wait_for_finger():
        print("Timeout: No finger detected")
        return None

    print("Image captured (1)")

    if finger.image_2_tz(1) != adafruit_fingerprint.OK:
        print("Failed to process image 1")
        return None


    print("Remove finger...")
    if not wait_for_removal():
        print("Timeout: Finger not removed")
        return None

    time.sleep(1)

    print("👉 Place SAME finger again...")
    if not wait_for_finger():
        print("Timeout: Second scan failed")
        return None

    print("Image captured (2)")

    if finger.image_2_tz(2) != adafruit_fingerprint.OK:
        print("Failed to process image 2")
        return None

    print("Creating fingerprint model...")
    if finger.create_model() != adafruit_fingerprint.OK:
        print("Failed to create model")
        return None

    if finger.read_templates() != adafruit_fingerprint.OK:
        print("Failed to read existing templates")
        return None

    location = None
    for i in range(1, 128):
        if i not in finger.templates:
            location = i
            break

    if location is None:
        print("Sensor memory full")
        return None

    print(f" Using slot: {location}")


    if finger.store_model(location) != adafruit_fingerprint.OK:
        print("Failed to store fingerprint")
        return None

    print(f"Fingerprint stored at ID {location}")

    return location

def match_fingerprint():
    print("\nMatching fingerprint...")

    if not wait_for_finger():
        print("No finger detected")
        return None

    print("Image captured")

    if finger.image_2_tz(1) != adafruit_fingerprint.OK:
        print("Failed to process image")
        return None

    if finger.finger_search() != adafruit_fingerprint.OK:
        print("Fingerprint not found")
        return None

    print(f"Match found: ID {finger.finger_id}")
    print(f"Confidence: {finger.confidence}")

    if finger.confidence < 40:
        print("Low confidence match")
        return None

    return finger.finger_id