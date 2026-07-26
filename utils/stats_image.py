from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import uuid
import os

BASE_IMAGE = "assets/stats.png"


def get_font(size):

    fonts = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
        "arial.ttf"
    ]

    for font in fonts:
        try:
            return ImageFont.truetype(font, size)
        except:
            continue

    return ImageFont.load_default()


def draw_text(
    draw,
    x,
    y,
    text,
    size,
    colour=(255, 255, 255)
):

    font = get_font(size)

    draw.text(
        (x, y),
        str(text),
        font=font,
        fill=colour,
        stroke_width=3,
        stroke_fill=(0, 0, 0)
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
    join_date
):

    image = Image.open(BASE_IMAGE).convert("RGBA")

    image = image.resize(
        (2560, 1440),
        Image.LANCZOS
    )

    draw = ImageDraw.Draw(image)

    width, height = image.size


    response = requests.get(
        avatar_url
    )

    avatar = Image.open(
        BytesIO(response.content)
    ).convert("RGBA")

    avatar = avatar.resize(
        (420, 420)
    )

    mask = Image.new(
        "L",
        (420, 420),
        0
    )

    ImageDraw.Draw(mask).ellipse(
        (0, 0, 420, 420),
        fill=255
    )

    image.paste(
        avatar,
        (120, 120),
        mask
    )


    draw_text(
        draw,
        650,
        120,
        username,
        120
    )

    draw_text(
        draw,
        650,
        330,
        f"Balance: {balance:,.2f}",
        70
    )

    draw_text(
        draw,
        650,
        430,
        f"Vault: {vault:,.2f}",
        70
    )

    draw_text(
        draw,
        650,
        530,
        f"Wagered: {wager:,.2f}",
        70
    )

    draw_text(
        draw,
        650,
        630,
        f"Deposited: {deposited:,.2f}",
        70
    )

    draw_text(
        draw,
        650,
        730,
        f"Withdrawn: {withdrawn:,.2f}",
        70
    )

    draw_text(
        draw,
        650,
        830,
        f"Affiliate: {affiliate:,.2f}",
        70
    )

    draw_text(
        draw,
        650,
        930,
        f"Joined: {join_date}",
        60
    )

    filename = f"stats_{uuid.uuid4().hex}.png"

    output = os.path.join(
        "assets",
        filename
    )

    image.save(output)

    return output
