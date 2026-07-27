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


def draw_text(draw, x, y, text, size, colour=(255,255,255)):
    draw.text(
        (x, y),
        str(text),
        font=get_font(size),
        fill=colour,
        stroke_width=3,
        stroke_fill=(0,0,0)
    )


def box(draw, x1, y1, x2, y2):
    draw.rounded_rectangle(
        (x1, y1, x2, y2),
        radius=18,
        fill=(25,35,55,220),
        outline=(80,120,255),
        width=2
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

    # ---------------- Username ----------------

    draw_text(
        draw,
        280,
        75,
        username,
        58
    )

    # ---------------- Boxes ----------------

    box(draw,60,290,610,360)
    box(draw,670,290,1220,360)

    box(draw,60,385,610,455)
    box(draw,670,385,1220,455)

    box(draw,60,480,610,550)
    box(draw,670,480,1220,550)

    box(draw,60,575,1220,650)

    # ---------------- Text ----------------

    draw_text(draw,90,305,f"Balance : £{balance:,.2f}",36)
    draw_text(draw,700,305,f"Vault : £{vault:,.2f}",36)

    draw_text(draw,90,400,f"Wagered : £{wager:,.2f}",36)
    draw_text(draw,700,400,f"Deposited : £{deposited:,.2f}",36)

    draw_text(draw,90,495,f"Withdrawn : £{withdrawn:,.2f}",36)
    draw_text(draw,700,495,f"Affiliate : £{affiliate:,.2f}",36)

    draw_text(draw,90,595,f"Joined : {join_date}",34)

    filename = f"stats_{uuid.uuid4().hex}.png"

    output = os.path.join(
        "assets",
        filename
    )

    image.save(output)

    return output
