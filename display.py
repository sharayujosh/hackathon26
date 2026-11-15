
import os
import sys
from PIL import Image, ImageDraw, ImageFont


# --------------------------------------------------
# WAVESHARE DRIVER
# --------------------------------------------------

BASE_DIR = (
    "/home/mahimndave/"
    "e-Paper/E-paper_Separate_Program/3in97_e-Paper_G/"
    "RaspberryPi_JetsonNano/python"
)

DRIVER_LIB = os.path.join(BASE_DIR, "lib")

if DRIVER_LIB not in sys.path:
    sys.path.insert(0, DRIVER_LIB)

from waveshare_epd import epd3in97g


# --------------------------------------------------
# FONTS
# --------------------------------------------------

def load_fonts():

    font_path = os.path.join(BASE_DIR, "pic", "Font.ttc")

    try:
        title_font = ImageFont.truetype(font_path, 34)
        detail_font = ImageFont.truetype(font_path, 25)
        heading_font = ImageFont.truetype(font_path, 26)
        item_font = ImageFont.truetype(font_path, 22)
        route_font = ImageFont.truetype(font_path, 23)

    except OSError:

        title_font = ImageFont.load_default()
        detail_font = ImageFont.load_default()
        heading_font = ImageFont.load_default()
        item_font = ImageFont.load_default()
        route_font = ImageFont.load_default()

    return (
        title_font,
        detail_font,
        heading_font,
        item_font,
        route_font
    )


# --------------------------------------------------
# UPDATE E-PAPER
# --------------------------------------------------

def update_screen(image):

    epd = epd3in97g.EPD()

    try:
        epd.init()
        epd.display(epd.getbuffer(image))
        epd.sleep()

    finally:
        epd3in97g.epdconfig.module_exit()


# --------------------------------------------------
# STATIC NAVIGATION SCREEN
# --------------------------------------------------

def show_navigation(
    patient_id,
    room,
    procedure,
    required_supplies,
    best_order,
    inventory
):

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    (
        title_font,
        detail_font,
        heading_font,
        item_font,
        route_font
    ) = load_fonts()

    epd = epd3in97g.EPD()

    image = Image.new(
        "RGB",
        (epd.height, epd.width),
        WHITE
    )

    draw = ImageDraw.Draw(image)

    # HEADER

    draw.rectangle(
        [(0, 0), (800, 55)],
        fill=BLACK
    )

    draw.text(
        (20, 8),
        "MEDROUTE NAVIGATION",
        font=title_font,
        fill=WHITE
    )

    # PATIENT INFORMATION

    draw.text(
        (20, 60),
        f"Patient No: {patient_id}",
        font=detail_font,
        fill=BLACK
    )

    draw.text(
        (20, 88),
        f"Patient Room: {room}",
        font=detail_font,
        fill=BLACK
    )

    draw.text(
        (20, 116),
        f"Procedure: {procedure}",
        font=detail_font,
        fill=BLACK
    )

    draw.line(
        [(20, 140), (780, 140)],
        fill=BLACK,
        width=2
    )

    # SUPPLY COLLECTION LIST

    draw.text(
        (20, 148),
        "SUPPLY COLLECTION LIST",
        font=heading_font,
        fill=BLACK
    )

    y_position = 181

    for number, supply in enumerate(required_supplies, start=1):

        draw.text(
            (30, y_position),
            f"{number}. {supply}",
            font=item_font,
            fill=BLACK
        )

        y_position += 22

    # ROUTE HEADING

    draw.line(
        [(20, 315), (780, 315)],
        fill=BLACK,
        width=2
    )

    draw.text(
        (20, 320),
        "ROUTE",
        font=heading_font,
        fill=BLACK
    )

    # ROUTE INSTRUCTIONS

    route_start = 350
    route_end = 438
    route_count = len(best_order)

    if route_count > 1:

        route_spacing = min(
            27,
            (route_end - route_start) // (route_count - 1)
        )

    else:

        route_spacing = 27

    y_position = route_start

    for number, location in enumerate(best_order, start=1):

        supply_name = inventory[location]["name"]

        instruction = (
            f"{number}. Collect {supply_name} from {location}"
        )

        draw.text(
            (30, y_position),
            instruction,
            font=route_font,
            fill=BLACK
        )

        y_position += route_spacing

    # FIXED BARCODE INSTRUCTION AT BOTTOM

    draw.rectangle(
        [(0, 465), (800, 495)],
        fill=BLACK
    )

    barcode_instruction = "SCAN THE BARCODE OF EACH REQUIRED ITEM"

    barcode_box = draw.textbbox(
        (0, 0),
        barcode_instruction,
        font=item_font
    )

    barcode_width = barcode_box[2] - barcode_box[0]

    draw.text(
        (20, 465),
        barcode_instruction,
        font=item_font,
        fill=WHITE
    )

    update_screen(image)


# --------------------------------------------------
# CLEAR E-PAPER SCREEN
# --------------------------------------------------

def clear_screen():

    WHITE = (255, 255, 255)

    epd = epd3in97g.EPD()

    # Create completely white image

    image = Image.new(
        "RGB",
        (epd.height, epd.width),
        WHITE
    )

    # Refresh display with blank image

    update_screen(image)


# --------------------------------------------------
# COMPLETION SCREEN
# --------------------------------------------------

def show_complete(patient_id, room, procedure):

    # Clear the display instead of showing a completion message.

    clear_screen()
