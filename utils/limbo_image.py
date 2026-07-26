from PIL import Image, ImageDraw, ImageFont
import os
import uuid


BASE_IMAGE = "assets/limbo.png"


def get_font(size):

    fonts = [
        "arial.ttf",
        "DejaVuSans-Bold.ttf"
    ]

    for font in fonts:
        try:
            return ImageFont.truetype(
                font,
                size
            )
        except:
            pass

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



    # Result text

    result_text = (
        "YOU WON"
        if won
        else
        "YOU LOST"
    )


    result_color = (
        (46,204,113)
        if won
        else
        (231,76,60)
    )



    multiplier_text = (
        f"{multiplier:.2f}x"
    )



    multiplier_font = get_font(
        2200
    )


    result_font = get_font(
        1100
    )



    # Center multiplier

    box = draw.textbbox(
        (0,0),
        multiplier_text,
        font=multiplier_font
    )


    text_width = (
        box[2] - box[0]
    )


    draw.text(
        (
            (width-text_width)//2,
            height//2-80
        ),
        multiplier_text,
        font=multiplier_font,
        fill=result_color
    )



    # Center win lose

    box = draw.textbbox(
        (0,0),
        result_text,
        font=result_font
    )


    text_width = (
        box[2]-box[0]
    )


    draw.text(
        (
            (width-text_width)//2,
            height//2+80
        ),
        result_text,
        font=result_font,
        fill=(255,255,255)
    )



    output = (
        f"limbo_{uuid.uuid4().hex}.png"
    )


    output_path = os.path.join(
        "assets",
        output
    )


    image.save(
        output_path
    )


    return output_path
