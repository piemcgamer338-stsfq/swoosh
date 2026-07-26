import re


def parse_time(value: str):

    value = value.lower().strip()

    match = re.fullmatch(
        r"(\d+)(s|m|h)",
        value
    )

    if not match:
        return None

    amount = int(match.group(1))
    unit = match.group(2)

    if unit == "s":
        seconds = amount

    elif unit == "m":
        seconds = amount * 60

    else:
        seconds = amount * 3600


    if seconds < 10:
        return None

    if seconds > 3600:
        return None

    return seconds



def format_time(seconds):

    hours = seconds // 3600
    seconds %= 3600

    minutes = seconds // 60
    seconds %= 60

    if hours:

        return (
            f"{hours:02}:{minutes:02}:{seconds:02}"
        )

    return (
        f"{minutes:02}:{seconds:02}"
    )
