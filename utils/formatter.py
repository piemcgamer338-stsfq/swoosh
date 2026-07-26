def number(value):

    if value >= 1000000:

        return f"{value/1000000:.2f}M"


    if value >= 1000:

        return f"{value/1000:.2f}K"


    return f"{value:,.2f}"



def points(value):

    return (
        f"🪙 {number(value)} Points"
    )



def usd(value):

    return (
        f"${value:,.2f}"
    )



def ltc(value):

    return (
        f"{value:.8f} LTC"
    )



def percent(value):

    return (
        f"{value:.2f}%"
    )



def signed(value):

    if value >= 0:

        return f"+{number(value)}"


    return f"-{number(abs(value))}"
