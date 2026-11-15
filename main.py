
import json
import os

import routing
import display
import barcode


# --------------------------------------------------
# LOAD DATABASE FILES
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def load_json(filename):

    filepath = os.path.join(BASE_DIR, filename)

    with open(filepath, "r") as file:
        return json.load(file)


INVENTORY = load_json("inventory.json")
PROCEDURES = load_json("procedures.json")
PATIENTS = load_json("patients.json")
NURSES = load_json("nurses.json")


# --------------------------------------------------
# CREATE SUPPLY BARCODE LOOKUP
# --------------------------------------------------

BARCODE_LOOKUP = {}

for storage_id, item_data in INVENTORY.items():

    barcode_value = str(item_data["barcode"])

    BARCODE_LOOKUP[barcode_value] = {
        "storage_id": storage_id,
        "name": item_data["name"]
    }


# --------------------------------------------------
# CREATE NURSE BARCODE LOOKUP
# --------------------------------------------------

NURSE_BARCODE_LOOKUP = {}

for nurse_barcode, nurse_data in NURSES.items():

    NURSE_BARCODE_LOOKUP[str(nurse_barcode)] = (nurse_data["nurse_id"])


# --------------------------------------------------
# FIND STORAGE LOCATIONS
# --------------------------------------------------

def find_supply_locations(required_supplies):

    supply_locations = []

    for supply in required_supplies:

        found_location = None

        for storage_id, item_data in INVENTORY.items():

            if item_data["name"] == supply:
                found_location = storage_id
                break

        if found_location is None:
            raise ValueError(
                f"Supply '{supply}' was not found in inventory."
            )

        supply_locations.append(found_location)

    return supply_locations


# --------------------------------------------------
# PROCESS ONE NURSE
# --------------------------------------------------

def process_nurse(nurse_id):

    # Check whether nurse exists in patient database
    if nurse_id not in PATIENTS:

        print("ERROR: Nurse ID not recognized.")
        return

    # Retrieve patient information
    patient_data = PATIENTS[nurse_id]

    patient_id = patient_data["patient_id"]
    patient_room = patient_data["room"]
    procedure_name = patient_data["procedure"]

    # Check whether procedure exists
    if procedure_name not in PROCEDURES:

        print("ERROR: Procedure not found.")
        return

    # Retrieve required supplies
    required_supplies = PROCEDURES[procedure_name]

    # Find storage locations
    storage_locations = find_supply_locations(required_supplies)

    # Calculate optimized route
    best_order, complete_path, total_distance = (routing.plan_multi_item_route(storage_locations))

    # --------------------------------------------------
    # DISPLAY NAVIGATION ONCE
    # --------------------------------------------------

    display.show_navigation(
        patient_id,
        patient_room,
        procedure_name,
        required_supplies,
        best_order,
        INVENTORY
    )

    print("\nPatient:", patient_id)
    print("Room:", patient_room)
    print("Procedure:", procedure_name)
    print("\nWaiting for supply barcodes...\n")

    # --------------------------------------------------
    # SUPPLY BARCODE COLLECTION
    # --------------------------------------------------

    collected_supplies = set()

    while len(collected_supplies) < len(required_supplies):

        # Wait for supply barcode
        scanned_barcode = str(barcode.scan_barcode()).strip()

        # Find scanned item
        scanned_item = BARCODE_LOOKUP.get(scanned_barcode)

        # Unknown barcode
        if scanned_item is None:
            print("ERROR: Unknown barcode.")
            continue

        supply_name = scanned_item["name"]

        # Check whether supply is required
        if supply_name not in required_supplies:
            print("ERROR: Wrong supply:", supply_name)
            continue

        # Check duplicate scan
        if supply_name in collected_supplies:
            print("Already collected:", supply_name)
            continue

        # Accept correct supply
        collected_supplies.add(supply_name)

        print("CORRECT:", supply_name, f"({len(collected_supplies)}/{len(required_supplies)})")

        # E-paper does not refresh during collection.

    # --------------------------------------------------
    # ALL SUPPLIES COLLECTED
    # --------------------------------------------------

    display.show_complete(
        patient_id,
        patient_room,
        procedure_name
    )

    print("\nAll supplies collected successfully.\n")


# --------------------------------------------------
# MAIN PROGRAM
# --------------------------------------------------

def main():

    while True:
        print("\n================================")
        print("       MEDROUTE NAVIGATION")
        print("================================")
        print("Scan Nurse ID Barcode:")

        # Scan nurse barcode
        scanned_nurse_barcode = str(
            barcode.scan_barcode()
        ).strip()

        # Identify nurse
        nurse_id = NURSE_BARCODE_LOOKUP.get(
            scanned_nurse_barcode
        )

        # Reject unrecognized nurse barcode
        if nurse_id is None:
            print("ERROR: Nurse barcode not recognized.")
            continue

        print("\nNurse identified:", nurse_id)

        # Start that nurse's collection process
        process_nurse(nurse_id)


# --------------------------------------------------
# START PROGRAM
# --------------------------------------------------

if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print("\nMedRoute Navigation stopped.")
