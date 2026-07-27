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
            requests.get(avatar_url).content
        )
    ).convert("RGBA")

    avatar = avatar.resize((110, 110))

    mask = Image.new("L", (110, 110), 0)

    ImageDraw.Draw(mask).ellipse(
        (0, 0, 110, 110),
        fill=255
    )

    image.paste(
        avatar,
        (55, 55),
        mask
    )

    draw_text(
        draw,
        190,
        68,
        username,
        28
    )

    draw_box(draw, 55, 225, 605, 285)
    draw_box(draw, 675, 225, 1225, 285)

    draw_box(draw, 55, 315, 605, 375)
    draw_box(draw, 675, 315, 1225, 375)

    draw_box(draw, 55, 405, 605, 465)
    draw_box(draw, 675, 405, 1225, 465)

    draw_text(
        draw,
        78,
        244,
        f"Balance : £{balance:,.2f}",
        18
    )

    draw_text(
        draw,
        698,
        244,
        f"Vault : £{vault:,.2f}",
        18
    )

    draw_text(
        draw,
        78,
        334,
        f"Wagered : £{wager:,.2f}",
        18
    )

    draw_text(
        draw,
        698,
        334,
        f"Deposited : £{deposited:,.2f}",
        18
    )

    draw_text(
        draw,
        78,
        424,
        f"Withdrawn : £{withdrawn:,.2f}",
        18
    )

    draw_text(
        draw,
        698,
        424,
        f"Affiliate : £{affiliate:,.2f}",
        18
    )

    filename = f"stats_{uuid.uuid4().hex}.png"

    output = os.path.join(
        "assets",
        filename
    )

    image.save(output)

    return outpu
