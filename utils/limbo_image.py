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



def fit_font(
    draw,
    text,
    max_width,
    start_size
):

    size = start_size

    while size > 10:

        font = get_font(size)

        box = draw.textbbox(
            (0,0),
            text,
            font=font
        )

        width = box[2] - box[0]

        if width <= max_width:
            return font

        size -= 5

    return get_font(10)



def center_position(
    draw,
    text,
    font,
    width
):

    box = draw.textbbox(
        (0,0),
        text,
        font=font
    )

    text_width = box[2] - box[0]

    return (width-text_width)//2



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



# EXTREME BIG TEXT

multiplier_font = get_font(450)
result_font = get_font(180)


multiplier_box = draw.textbbox(
    (0, 0),
    multiplier_text,
    font=multiplier_font
)

multiplier_width = multiplier_box[2] - multiplier_box[0]


draw.text(
    (
        (width - multiplier_width) // 2,
        height * 0.18
    ),
    multiplier_text,
    font=multiplier_font,
    fill=multiplier_color,
    stroke_width=12,
    stroke_fill=(0,0,0)
)



result_box = draw.textbbox(
    (0, 0),
    result_text,
    font=result_font
)

result_width = result_box[2] - result_box[0]


draw.text(
    (
        (width-result_width)//2,
        height * 0.70
    ),
    result_text,
    font=result_font,
    fill=(255,255,255),
    stroke_width=8,
    stroke_fill=(0,0,0)
)


    # win lose

    x = center_position(
        draw,
        result_text,
        result_font,
        width
    )


    draw.text(
        (
            x,
            height * 0.70
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
