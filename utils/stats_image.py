from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import uuid
import os

BASE_IMAGE = "assets/stats.png"

CARD_BG = (18, 29, 48, 210)
CARD_BORDER = (80, 120, 255, 120)
WHITE = (255,255,255)
GRAY = (180,190,210)
GREEN = (46,204,113)
BLUE = (52,152,219)


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
            continue

    return ImageFont.load_default()


def draw_text(
    draw,
    x,
    y,
    text,
    size,
    colour=WHITE
):

    draw.text(
        (x,y),
        str(text),
        font=get_font(size),
        fill=colour,
        stroke_width=3,
        stroke_fill=(0,0,0)
    )


def rounded_box(
    draw,
    xy,
    radius=18
):

    draw.rounded_rectangle(
        xy,
        radius=radius,
        fill=CARD_BG,
        outline=CARD_BORDER,
        width=2
    )


def profile_picture(
    image,
    url
):

    avatar = Image.open(
        BytesIO(
            requests.get(url).content
        )
    ).convert("RGBA")

    avatar = avatar.resize((180,180))

    mask = Image.new(
        "L",
        (180,180),
        0
    )

    ImageDraw.Draw(mask).ellipse(
        (0,0,180,180),
        fill=255
    )

    image.paste(
        avatar,
        (60,60),
        mask
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

    image = Image.open(
        BASE_IMAGE
    ).convert("RGBA")

    draw = ImageDraw.Draw(image)

    profile_picture(
        image,
        avatar_url
    )

    # ===========================
    # Header
    # ===========================

    draw_text(
        draw,
        270,
        70,
        username,
        54
    )

    draw_text(
        draw,
        270,
        135,
        "Casino Profile",
        24,
        GRAY
    )

    # ===========================
    # Left Column
    # ===========================

    rounded_box(
        draw,
        (50,300,610,380)
    )

    draw_text(
        draw,
        80,
        320,
        "💰 Balance",
        28,
        GRAY
    )

    draw_text(
        draw,
        80,
        345,
        f"£{balance:,.2f}",
        42,
        GREEN
    )


    rounded_box(
        draw,
        (50,400,610,480)
    )

    draw_text(
        draw,
        80,
        420,
        "🏦 Vault",
        28,
        GRAY
    )

    draw_text(
        draw,
        80,
        445,
        f"£{vault:,.2f}",
        42,
        BLUE
    )


    rounded_box(
        draw,
        (50,500,610,580)
    )

    draw_text(
        draw,
        80,
        520,
        "🎲 Total Wagered",
        28,
        GRAY
    )

    draw_text(
        draw,
        80,
        545,
        f"£{wager:,.2f}",
        38
    )


    # ===========================
    # Right Column
    # ===========================

    rounded_box(
        draw,
        (670,300,1230,380)
    )

    draw_text(
        draw,
        700,
        320,
        "📥 Deposited",
        28,
        GRAY
    )

    draw_text(
        draw,
        700,
        345,
        f"£{deposited:,.2f}",
        38
    )


    rounded_box(
        draw,
        (670,400,1230,480)
    )

    draw_text(
        draw,
        700,
        420,
        "📤 Withdrawn",
        28,
        GRAY
    )

    draw_text(
        draw,
        700,
        445,
        f"£{withdrawn:,.2f}",
        38
    )


    rounded_box(
        draw,
        (670,500,1230,580)
    )

    draw_text(
        draw,
        700,
        520,
        "🤝 Affiliate",
        28,
        GRAY
    )

    draw_text(
        draw,
        700,
        545,
        f"£{affiliate:,.2f}",
        38
    )


    rounded_box(
        draw,
        (50,610,1230,690)
    )

    draw_text(
        draw,
        80,
        635,
        "📅 Joined",
        26,
        GRAY
    )

    draw_text(
        draw,
        260,
        635,
        join_date,
        30
    )
        # ===========================
    # Footer
    # ===========================

    draw.line(
        (50, 705, 1230, 705),
        fill=(70, 90, 140),
        width=2
    )

    draw_text(
        draw,
        70,
        715,
        "Swoosh Casino",
        22,
        (150,170,220)
    )

    draw_text(
        draw,
        1020,
        715,
        "Profile Card",
        22,
        (150,170,220)
    )

    # ===========================
    # Save image
    # ===========================

    filename = f"stats_{uuid.uuid4().hex}.png"

    output_path = os.path.join(
        "assets",
        filename
    )

    image.save(
        output_path,
        quality=100
    )

    return output_path
