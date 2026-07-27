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
    # ---------------- Avatar ----------------

    response = requests.get(avatar_url)

    avatar = Image.open(
        BytesIO(response.content)
    ).convert("RGBA")

    avatar = avatar.resize((220,220))

    mask = Image.new("L", (220,220), 0)

    ImageDraw.Draw(mask).ellipse(
        (0,0,220,220),
        fill=255
    )

    image.paste(
        avatar,
        (65,45),
        mask
    )

    # ---------------- Username ----------------

    draw_text(
        draw,
        310,
        95,
        username,
        50
    )

    # ---------------- Boxes ----------------

    box(draw,60,265,610,345)
    box(draw,670,265,1220,345)

    box(draw,60,365,610,445)
    box(draw,670,365,1220,445)

    box(draw,60,465,610,545)
    box(draw,670,465,1220,545)

    box(draw,60,565,1220,645)

    # ---------------- Text ----------------

    draw_text(
        draw,
        95,
        292,
        f"Balance : £{balance:,.2f}",
        34
    )

    draw_text(
        draw,
        705,
        292,
        f"Vault : £{vault:,.2f}",
        34
    )

    draw_text(
        draw,
        95,
        392,
        f"Wagered : £{wager:,.2f}",
        34
    )

    draw_text(
        draw,
        705,
        392,
        f"Deposited : £{deposited:,.2f}",
        34
    )

    draw_text(
        draw,
        95,
        492,
        f"Withdrawn : £{withdrawn:,.2f}",
        34
    )

    draw_text(
        draw,
        705,
        492,
        f"Affiliate : £{affiliate:,.2f}",
        34
    )

    draw_text(
        draw,
        95,
        592,
        f"Joined : {join_date}",
        32
    )
    
    image = Image.open(BASE_IMAGE).convert("RGBA")
    draw = ImageDraw.Draw(image)


    filename = f"stats_{uuid.uuid4().hex}.png"

    output = os.path.join(
        "assets",
        filename
    )

    image.save(output)

    return output
