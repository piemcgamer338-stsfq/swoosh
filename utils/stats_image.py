from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import uuid
import os

BASE_IMAGE = "assets/stats.png"


def font(size):
    fonts = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
        "arial.ttf"
    ]

    for f in fonts:
        try:
            return ImageFont.truetype(f, size)
        except:
            continue

    return ImageFont.load_default()


def text(draw, x, y, value, size, colour=(255,255,255)):

    draw.text(
        (x, y),
        str(value),
        font=font(size),
        fill=colour,
        stroke_width=5,
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


    # ---------------- Avatar ----------------

    avatar = Image.open(
        BytesIO(
            requests.get(avatar_url).content
        )
    ).convert("RGBA")

    avatar = avatar.resize((260,260))

    mask = Image.new("L",(260,260),0)
    ImageDraw.Draw(mask).ellipse((0,0,260,260),fill=255)

    image.paste(
        avatar,
        (80,70),
        mask
    )


    # ---------------- Username ----------------

    text(
        draw,
        390,
        70,
        username,
        95
    )


    # ---------------- Stats ----------------

    text(draw,390,220,f"Balance : {balance:,.2f}",65)
    text(draw,390,305,f"Vault : {vault:,.2f}",65)
    text(draw,390,390,f"Wagered : {wager:,.2f}",65)
    text(draw,390,475,f"Deposited : {deposited:,.2f}",65)
    text(draw,390,560,f"Withdrawn : {withdrawn:,.2f}",65)
    text(draw,390,645,f"Affiliate : {affiliate:,.2f}",65)
    text(draw,390,730,f"Joined : {join_date}",60)


    filename=f"stats_{uuid.uuid4().hex}.png"

    path=os.path.join(
        "assets",
        filename
    )

    image.save(path)

    return path
