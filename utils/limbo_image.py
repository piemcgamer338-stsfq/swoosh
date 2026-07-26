from PIL import Image, ImageDraw, ImageFont
import os
import uuid


BASE_IMAGE = "assets/limbo.png"


def get_font(size):

    fonts = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
        "arial.ttf"
    ]

    for font in fonts:
        try:
            return ImageFont.truetype(
                font,
                size
            )
        except:
            continue

    return ImageFont.load_default()



def create_limbo_image(
    multiplier,
    won
):

    if not os.path.exists(BASE_IMAGE):

        raise FileNotFoundError(
            "assets/limbo.png not found"
        )


    image = Image.open(
        BASE_IMAGE
    ).convert(
        "RGBA"
    )


    draw = ImageDraw.Draw(
        image
    )


    width, height = image.size



    multiplier_text = (
        f"{multiplier:.2f}x"
    )


    result_text = (
        "YOU WON"
        if won
        else
        "YOU LOST"
    )


    multiplier_color = (
        (46,204,113)
        if won
        else
        (231,76,60)
    )



    # BIG CASINO TEXT

    multiplier_font = get_font(
        450
    )


    result_font = get_font(
        180
    )



    # MULTIPLIER TEXT

    box = draw.textbbox(
        (0,0),
        multiplier_text,
        font=multiplier_font
    )


    multiplier_width = (
        box[2] - box[0]
    )


    draw.text(
        (
            (width - multiplier_width)//2,
            height * 0.15
        ),
        multiplier_text,
        font=multiplier_font,
        fill=multiplier_color,
        stroke_width=12,
        stroke_fill=(0,0,0)
    )



    # WIN / LOSE TEXT

    box = draw.textbbox(
        (0,0),
        result_text,
        font=result_font
    )


    result_width = (
        box[2] - box[0]
    )


    draw.text(
        (
            (width-result_width)//2,
            height * 0.72
        ),
        result_text,
        font=result_font,
        fill=(255,255,255),
        stroke_width=8,
        stroke_fill=(0,0,0)
    )



    filename = (
        f"limbo_{uuid.uuid4().hex}.png"
    )


    path = os.path.join(
        "assets",
        filename
    )


    image.save(
        path
    )


    return path
