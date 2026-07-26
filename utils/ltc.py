from utils.constants import POINT_VALUE



def points_to_ltc(points, ltc_price):

    usd = points * POINT_VALUE

    return usd / ltc_price



def ltc_to_points(
    ltc_amount,
    ltc_price
):

    usd = ltc_amount * ltc_price

    return usd / POINT_VALUE



def format_ltc(amount):

    return (
        f"{amount:.8f} LTC"
    )



def validate_ltc_address(address):

    if not address:

        return False


    # Litecoin legacy + M addresses
    if (
        address.startswith("L")
        or
        address.startswith("M")
    ):

        return True


    return False



def minimum_deposit_check(
    amount
):

    return amount >= 0.10



def minimum_withdraw_check(
    amount
):

    return amount >= 1.00
