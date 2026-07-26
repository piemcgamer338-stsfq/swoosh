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


def draw_text(draw, x, y, text, size, colour=(255,255,255)):

    font = get_font(size)

    draw.text(
        (x, y),
        str(text),
        font=font,
        fill=colour,
        stroke_width=4,
        stroke_fill=(0,0,0)
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

    width, height = image.size


    response = requests.get(avatar_url)

    avatar = Image.open(
        BytesIO(response.content)
    ).convert("RGBA")

    avatar = avatar.resize((180,180))

    mask = Image.new("L",(180,180),0)

    ImageDraw.Draw(mask).ellipse(
        (0,0,180,180),
        fill=255
    )

    image.paste(
        avatar,
        (60,60),
        mask
    )


    # HUGE username
    draw_text(
        draw,
        280,
        55,
        username,
        72
    )

    # VERY BIG stats
    draw_text(draw,280,180,f"Balance: {balance:,.2f}",52)
    draw_text(draw,280,245,f"Vault: {vault:,.2f}",52)
    draw_text(draw,280,310,f"Wagered: {wager:,.2f}",52)
    draw_text(draw,280,375,f"Deposited: {deposited:,.2f}",52)
    draw_text(draw,280,440,f"Withdrawn: {withdrawn:,.2f}",52)
    draw_text(draw,280,505,f"Affiliate: {affiliate:,.2f}",52)
    draw_text(draw,280,570,f"Joined: {join_date}",48)


    filename=f"stats_{uuid.uuid4().hex}.png"

    path=os.path.join(
        "assets",
        filename
    )

    image.save(path)

    return path
