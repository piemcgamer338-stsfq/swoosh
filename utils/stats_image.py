from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import requests
import uuid
import os

BASE_IMAGE = "assets/stats.png"


def get_font(size):
    fonts = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
        "arial.ttf",
    ]

    for f in fonts:
        try:
            return ImageFont.truetype(f, size)
        except:
            pass

    return ImageFont.load_default()


def rounded_box(draw, x1, y1, x2, y2):
    draw.rounded_rectangle(
        (x1, y1, x2, y2),
        radius=18,
        fill=(25, 35, 55, 230),
        outline=(70, 110, 220),
        width=2,
    )


def write(draw, x, y, text, size, colour=(255, 255, 255)):
    draw.text(
        (x, y),
        str(text),
        font=get_font(size),
        fill=colour,
    )


def create_stats_image(
    avatar_url,
    username,
    balance,
    vault,
    wager,
    deposited,
    withdrawn,
    affiliate,
    joined,
):

    image = Image.open(BASE_IMAGE).convert("RGBA")
    draw = ImageDraw.Draw(image)

    # Avatar
    avatar = Image.open(
        BytesIO(requests.get(avatar_url).content)
    ).convert("RGBA")

    avatar = avatar.resize((200, 200))

    mask = Image.new("L", (200, 200), 0)

    ImageDraw.Draw(mask).ellipse(
        (0, 0, 200, 200),
        fill=255,
    )

    image.paste(
        avatar,
        (55, 45),
        mask,
    )

    # Username

    write(
        draw,
        290,
        90,
        username,
        46,
    )

    # Boxes

    rounded_box(draw, 50, 260, 610, 340)
    rounded_box(draw, 670, 260, 1230, 340)

    rounded_box(draw, 50, 360, 610, 440)
    rounded_box(draw, 670, 360, 1230, 440)

    rounded_box(draw, 50, 460, 610, 540)
    rounded_box(draw, 670, 460, 1230, 540)

    rounded_box(draw, 50, 560, 1230, 640)
        # ---------------- Text ----------------

    write(
        draw,
        95,
        292,
        f"Balance : £{balance:,.2f}",
        34,
    )

    write(
        draw,
        705,
        292,
        f"Vault : £{vault:,.2f}",
        34,
    )

    write(
        draw,
        95,
        392,
        f"Wagered : £{wager:,.2f}",
        34,
    )

    write(
        draw,
        705,
        392,
        f"Deposited : £{deposited:,.2f}",
        34,
    )

    write(
        draw,
        95,
        492,
        f"Withdrawn : £{withdrawn:,.2f}",
        34,
    )

    write(
        draw,
        705,
        492,
        f"Affiliate : £{affiliate:,.2f}",
        34,
    )

    write(
        draw,
        95,
        592,
        f"Joined : {joined}",
        30,
    )

    filename = f"stats_{uuid.uuid4().hex}.png"

    output = os.path.join(
        "assets",
        filename,
    )

    image.save(output)

    return output
