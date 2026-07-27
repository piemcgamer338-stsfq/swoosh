from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from io import BytesIO
import requests
import uuid
import os

BASE_IMAGE = "assets/stats.png"


def font(size):

    try:
        return ImageFont.truetype(
            "arial.ttf",
            size
        )

    except:

        return ImageFont.load_default()


def rounded(
    draw,
    x1,
    y1,
    x2,
    y2
):

    draw.rounded_rectangle(
        (
            x1,
            y1,
            x2,
            y2
        ),
        radius=20,
        fill=(20, 25, 35),
        outline=(65, 120, 255),
        width=3
    )


def text(
    draw,
    x,
    y,
    value,
    size
):

    draw.text(
        (
            x,
            y
        ),
        str(value),
        fill="white",
        font=font(size)
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

    image = Image.open(
        BASE_IMAGE
    ).convert(
        "RGBA"
    )

    draw = ImageDraw.Draw(
        image
    )

    avatar = Image.open(
        BytesIO(
            requests.get(
                avatar_url
            ).content
        )
    ).convert(
        "RGBA"
    )

    avatar = avatar.resize(
        (
            190,
            190
        )
    )

    mask = Image.new(
        "L",
        (
            190,
            190
        ),
        0
    )

    ImageDraw.Draw(
        mask
    ).ellipse(
        (
            0,
            0,
            190,
            190
        ),
        fill=255
    )

    image.paste(
        avatar,
        (
            65,
            55
        ),
        mask
    )

    text(
        draw,
        300,
        95,
        username,
        48
    )

    rounded(draw,60,270,610,345)
    rounded(draw,670,270,1220,345)

    rounded(draw,60,365,610,440)
    rounded(draw,670,365,1220,440)

    rounded(draw,60,460,610,535)
    rounded(draw,670,460,1220,535)

    text(
        draw,
        95,
        292,
        f"Balance : £{balance:,.2f}",
        34
    )

    text(
        draw,
        705,
        292,
        f"Vault : £{vault:,.2f}",
        34
    )

    text(
        draw,
        95,
        387,
        f"Wagered : £{wager:,.2f}",
        34
    )

    text(
        draw,
        705,
        387,
        f"Deposited : £{deposited:,.2f}",
        34
    )

    text(
        draw,
        95,
        482,
        f"Withdrawn : £{withdrawn:,.2f}",
        34
    )

    text(
        draw,
        705,
        482,
        f"Affiliate : £{affiliate:,.2f}",
        34
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
