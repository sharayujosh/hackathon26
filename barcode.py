from evdev import InputDevice, categorize, ecodes

# USB barcode scanner
SCANNER_PATH = "/dev/input/by-id/usb-NEWTOLOGIC_NEWTOLOGIC-event-kbd"


def scan_barcode():

    scanner = InputDevice(SCANNER_PATH)

    barcode = ""

    try:
        for event in scanner.read_loop():

            if event.type == ecodes.EV_KEY:

                key = categorize(event)

                # Only process key presses, not releases
                if key.keystate != key.key_down:
                    continue

                key_name = key.keycode

                # Barcode is complete when Enter is pressed
                if key_name == "KEY_ENTER":
                    if barcode:
                        return barcode

                # Convert number keys into actual digits
                elif key_name.startswith("KEY_"):

                    value = key_name.replace("KEY_", "")

                    if value.isdigit():
                        barcode += value

    finally:
        scanner.close()


# Standalone test
if __name__ == "__main__":

    while True:

        print("Waiting for barcode scan...")

        result = scan_barcode()

        print("Barcode received:", result)

