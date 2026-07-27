from PIL import Image
import os
import uuid

# Folder containing all card PNGs
CARD_FOLDER = "assets/cards"

# Background image
BACKGROUND = "assets/blackjack_table.png"


CARD_WIDTH = 90
CARD_HEIGHT = 130

DEALER_X = 85
DEALER_Y = 25
DEALER_SPACING = 42

PLAYER_X = 85
PLAYER_Y = 180
PLAYER_SPACING = 42


def load_card(card):

    path = os.path.join(
        CARD_FOLDER,
        f"{card}.png"
    )

    img = Image.open(path).convert("RGBA")

    img = img.resize(
        (
            CARD_WIDTH,
            CARD_HEIGHT
        )
    )

    return img


def load_back():

    path = os.path.join(
        CARD_FOLDER,
        "back.png"
    )

    img = Image.open(path).convert("RGBA")

    img = img.resize(
        (
            CARD_WIDTH,
            CARD_HEIGHT
        )
    )

    return img


def create_blackjack_image(

    player_hand,
    dealer_hand,

    hide_dealer=True

):

    image = Image.open(
        BACKGROUND
    ).convert("RGBA")

    # ---------- Dealer ----------

    x = DEALER_X

    for i, card in enumerate(dealer_hand):

        if i == 1 and hide_dealer:

            img = load_back()

        else:

            img = load_card(card)

        image.paste(

            img,

            (
                x,
                DEALER_Y
            ),

            img

        )

        x += DEALER_SPACING

    # ---------- Player ----------

    x = PLAYER_X

    for card in player_hand:

        img = load_card(card)

        image.paste(

            img,

            (
                x,
                PLAYER_Y
            ),

            img

        )

        x += PLAYER_SPACING

    filename = f"bj_{uuid.uuid4().hex}.png"

    output = os.path.join(

        "assets",

        filename

    )

    image.save(output)

    return output
