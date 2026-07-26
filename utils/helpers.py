from datetime import datetime, timedelta


POINT_VALUE = 0.005


def format_points(amount):
    return f"{amount:,.2f} Points"



def points_to_usd(points):
    return points * POINT_VALUE



def usd_to_points(usd):
    return usd / POINT_VALUE



def format_money(amount):
    return f"${amount:,.2f}"



def percentage(amount, percent):
    return amount * (percent / 100)



def cooldown_remaining(last_time, cooldown):

    if not last_time:
        return 0

    now = datetime.utcnow()

    difference = now - last_time

    if difference >= cooldown:
        return 0

    remaining = cooldown - difference

    return int(remaining.total_seconds())



def format_time(seconds):

    if seconds <= 0:
        return "Ready"

    minutes, seconds = divmod(seconds, 60)

    hours, minutes = divmod(minutes, 60)

    if hours:
        return f"{hours}h {minutes}m"

    if minutes:
        return f"{minutes}m {seconds}s"

    return f"{seconds}s"



def progress_bar(current, maximum, length=10):

    if maximum <= 0:
        return "⬜" * length

    percentage_value = min(current / maximum, 1)

    filled = int(
        percentage_value * length
    )

    return (
        "🟩" * filled
        +
        "⬜" * (length - filled)
    )



def get_rank(wager):

    ranks = [
        ("Bronze", 0),
        ("Silver", 100),
        ("Gold", 500),
        ("Platinum", 1000),
        ("Diamond", 2500),
        ("Master", 5000),
        ("Legend", 10000),
        ("Champion", 25000)
    ]


    current = "Bronze"

    for name, requirement in ranks:

        if wager >= requirement:
            current = name

    return current
