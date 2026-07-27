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
        "arial.ttf"
    ]

    for f in fonts:
        try:
            return ImageFont.truetype(f, size)
        except:
            pass

    return ImageFont.load_default()


def draw_box(draw, x1, y1, x2, y2):
    draw.rounded_rectangle(
        (x1, y1, x2, y2),
        radius=18,
        fill=(22, 28, 42, 235),
        outline=(70, 130, 255),
        width=3
    )


def draw_text(draw, x, y, txt, size):
    draw.text(
        (x, y),
        str(txt),
        font=get_font(size),
        fill="white"
    )


def create_stats_image(
    avatar_url,
    username,
    balance,
    vault,
    wager,
    deposited,
    withdrawn,
    affiliate
):

    image = Image.open(BASE_IMAGE).convert("RGBA")
    draw = ImageDraw.Draw(image)

    avatar = Image.open(
        BytesIO(
            requests.get(
                avatar_url
            ).content
        )
    ).convert("RGBA")

    avatar = avatar.resize((145, 145))

    mask = Image.new(
        "L",
        (145, 145),
        0
    )

    ImageDraw.Draw(mask).ellipse(
        (0, 0, 145, 145),
        fill=255
    )

    image.paste(
        avatar,
        (55, 40),
        mask
    )

    draw_text(
        draw,
        225,
        70,
        username,
        34
    )

    draw_box(draw, 40, 235, 605, 300)
    draw_box(draw, 675, 235, 1240, 300)

    draw_box(draw, 40, 325, 605, 390)
    draw_box(draw, 675, 325, 1240, 390)

    draw_box(draw, 40, 415, 605, 480)
    draw_box(draw, 675, 415, 1240, 480)
       
    draw_text(
        draw,
        65,
        252,
        f"Balance : £{balance:,.2f}",
        24
    )

    draw_text(
        draw,
        700,
        252,
        f"Vault : £{vault:,.2f}",
        24
    )

    draw_text(
        draw,
        65,
        342,
        f"Wagered : £{wager:,.2f}",
        24
    )

    draw_text(
        draw,
        700,
        342,
        f"Deposited : £{deposited:,.2f}",
        24
    )

    draw_text(
        draw,
        65,
        432,
        f"Withdrawn : £{withdrawn:,.2f}",
        24
    )

    draw_text(
        draw,
        700,
        432,
        f"Affiliate : £{affiliate:,.2f}",
        24
    )

    filename = f"stats_{uuid.uuid4().hex}.png"

    output = os.path.join(
        "assets",
        filename
    )

    image.save(
        output
    )

    return output
