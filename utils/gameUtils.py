def calculate_profit(bet, multiplier):

    return (bet * multiplier) - bet



def calculate_payout(bet, multiplier):

    return bet * multiplier



def valid_bet(amount):

    return amount > 0



def format_multiplier(value):

    return f"{value:.2f}x"



def clamp(value, minimum, maximum):

    return max(
        minimum,
        min(value, maximum)
    )
