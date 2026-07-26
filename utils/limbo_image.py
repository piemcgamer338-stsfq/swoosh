from PIL import Image, ImageDraw, ImageFont
import os
import uuid


BASE_IMAGE = "assets/limbo.png"


def get_font(size):

    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "DejaVuSans-Bold.ttf",
        "arial.ttf"
    ]

    for path in paths:
        try:
            return ImageFont.truetype(
                path,
                size
            )
        except:
            continue

    return ImageFont.load_default()



def center_text(draw, text, font, width):

    box = draw.textbbox(
        (0, 0),
        text,
        font=font
    )

    return (width - (box[2] - box[0])) // 2



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



    result_text = (
        "YOU WON"
        if won
        else "YOU LOST"
    )


    result_color = (
        (46,204,113)
        if won
        else (231,76,60)
    )


    multiplier_text = (
        f"{multiplier:.2f}x"
    )



    # Dynamic sizing based on image size

    multiplier_font = get_font(
        int(height * 0.32)
    )


    result_font = get_font(
        int(height * 0.12)
    )



    # multiplier

    x = center_text(
        draw,
        multiplier_text,
        multiplier_font,
        width
    )


    draw.text(
        (
            x,
            int(height * 0.25)
        ),
        multiplier_text,
        font=multiplier_font,
        fill=result_color,
        stroke_width=3,
        stroke_fill=(0,0,0)
    )



    # win/loss

    x = center_text(
        draw,
        result_text,
        result_font,
        width
    )


    draw.text(
        (
            x,
            int(height * 0.65)
        ),
        result_text,
        font=result_font,
        fill=(255,255,255),
        stroke_width=3,
        stroke_fill=(0,0,0)
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
