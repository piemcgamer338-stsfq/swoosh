from PIL import Image, ImageDraw, ImageFont
import os


ASSET_PATH = "assets"



def get_font(size=40):

    font_path = (
        "assets/fonts/arial.ttf"
    )

    if os.path.exists(font_path):

        return ImageFont.truetype(
            font_path,
            size
        )

    return ImageFont.load_default()



def create_canvas(
    width=900,
    height=500,
    colour=(15,15,20)
):

    image = Image.new(
        "RGB",
        (width,height),
        colour
    )

    return image



def add_text(
    image,
    text,
    position,
    size=40
):

    draw = ImageDraw.Draw(image)

    draw.text(
        position,
        text,
        font=get_font(size),
        fill=(255,255,255)
    )



def save_image(
    image,
    name
):

    os.makedirs(
        ASSET_PATH,
        exist_ok=True
    )


    path = (
        f"{ASSET_PATH}/{name}.png"
    )


    image.save(path)

    return path



def create_coinflip_result(
    result
):

    image = create_canvas()


    add_text(
        image,
        f"Coin landed: {result}",
        (200,220),
        50
    )


    return save_image(
        image,
        "coinflip_result"
    )



def create_limbo_result(
    multiplier,
    crashed=False
):

    image = create_canvas()


    status = (
        "CRASHED"
        if crashed
        else "SUCCESS"
    )


    add_text(
        image,
        f"{status}  {multiplier}x",
        (250,220),
        50
    )


    return save_image(
        image,
        "limbo_result"
    )
