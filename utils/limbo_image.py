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



def center_x(draw, text, font, width):

    box = draw.textbbox(
        (0, 0),
        text,
        font=font
    )

    text_width = box[2] - box[0]

    return (width - text_width) // 2



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


    multiplier_text = f"{multiplier:.2f}x"


    result_text = (
        "YOU WON"
        if won
        else
        "YOU LOST"
    )


    multiplier_color = (
        (46, 204, 113)
        if won
        else
        (231, 76, 60)
    )



    # 10x BIGGER VERSION

    multiplier_font = get_font(
        int(height * 3.0)
    )


    result_font = get_font(
        int(height * 0.65)
    )



    # MULTIPLIER

    x = center_x(
        draw,
        multiplier_text,
        multiplier_font,
        width
    )


    draw.text(
        (
            x,
            int(height * 0.10)
        ),
        multiplier_text,
        font=multiplier_font,
        fill=multiplier_color,
        stroke_width=20,
        stroke_fill=(0,0,0)
    )



    # WIN / LOSE

    x = center_x(
        draw,
        result_text,
        result_font,
        width
    )


    draw.text(
        (
            x,
            int(height * 0.75)
        ),
        result_text,
        font=result_font,
        fill=(255,255,255),
        stroke_width=15,
        stroke_fill=(0,0,0)
    )



    filename = f"limbo_{uuid.uuid4().hex}.png"


    output_path = os.path.join(
        "assets",
        filename
    )


    image.save(
        output_path
    )


    return output_path
