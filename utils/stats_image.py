from PIL import Image, ImageDraw, ImageFont
import requests
import uuid
import os
from io import BytesIO

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


def draw_text(draw, x, y, text, size, colour=(255, 255, 255)):

    font = get_font(size)

    draw.text(
        (x, y),
        str(text),
        font=font,
        fill=colour,
        stroke_width=2,
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
    draw = ImageDraw.Draw(image)

    # Avatar

    response = requests.get(avatar_url)

    avatar = Image.open(
        BytesIO(response.content)
    ).convert("RGBA")

    avatar = avatar.resize((220, 220))

    mask = Image.new(
        "L",
        (220, 220),
        0
    )

    ImageDraw.Draw(mask).ellipse(
        (0, 0, 220, 220),
        fill=255
    )

    image.paste(
        avatar,
        (70, 80),
        mask
    )

    # Username

    draw_text(
        draw,
        330,
        90,
        username,
        70
    )

    # Stats

    draw_text(draw, 330, 220, f"Balance: {balance:,.2f}", 42)
    draw_text(draw, 330, 285, f"Vault: {vault:,.2f}", 42)
    draw_text(draw, 330, 350, f"Wagered: {wager:,.2f}", 42)
    draw_text(draw, 330, 415, f"Deposited: {deposited:,.2f}", 42)
    draw_text(draw, 330, 480, f"Withdrawn: {withdrawn:,.2f}", 42)
    draw_text(draw, 330, 545, f"Affiliate: {affiliate:,.2f}", 42)
    draw_text(draw, 330, 610, f"Joined: {join_date}", 38)

    filename = f"stats_{uuid.uuid4().hex}.png"

    path = os.path.join(
        "assets",
        filename
    )

    image.save(path)

    return path
