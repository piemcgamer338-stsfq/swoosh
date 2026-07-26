from PIL import Image
import os
import uuid


CARD_FOLDER = "assets/cards"


def create_hilo_image(
    card
):

    path = os.path.join(
        CARD_FOLDER,
        card.filename
    )


    if not os.path.exists(path):

        raise FileNotFoundError(
            f"{path} not found."
        )


    image = Image.open(
        path
    ).convert(
        "RGBA"
    )


    output = os.path.join(
        "assets",
        f"hilo_{uuid.uuid4().hex}.png"
    )


    image.save(
        output
    )


    return output
