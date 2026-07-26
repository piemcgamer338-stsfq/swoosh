import hashlib
import secrets
import hmac



def generate_server_seed():

    return secrets.token_hex(32)



def hash_server_seed(server_seed):

    return hashlib.sha256(
        server_seed.encode()
    ).hexdigest()



def generate_client_seed():

    return secrets.token_hex(16)



def generate_game_id():

    return secrets.token_hex(8)



def generate_result(
    server_seed,
    client_seed,
    nonce
):

    message = (
        f"{client_seed}:{nonce}"
    )

    result = hmac.new(
        server_seed.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()

    return result



def number_from_hash(hash_result):

    return int(
        hash_result[:8],
        16
    )



# =====================
# COINFLIP
# =====================

def coinflip_result(
    server_seed,
    client_seed,
    nonce
):

    hash_result = generate_result(
        server_seed,
        client_seed,
        nonce
    )

    number = number_from_hash(
        hash_result
    )

    if number % 2 == 0:

        return "heads"

    return "tails"



# =====================
# DICE 1-100
# =====================

def dice_result(
    server_seed,
    client_seed,
    nonce
):

    data = (
        f"{server_seed}:{client_seed}:{nonce}:dice"
    )


    hash_result = hashlib.sha256(
        data.encode()
    ).hexdigest()


    number = int(
        hash_result[:8],
        16
    )


    return (number % 100) + 1



# =====================
# LIMBO
# =====================

def limbo_result(
    server_seed,
    client_seed,
    nonce
):

    data = (
        f"{server_seed}:{client_seed}:{nonce}:limbo"
    )


    hash_result = hmac.new(
        server_seed.encode(),
        data.encode(),
        hashlib.sha256
    ).hexdigest()


    number = int(
        hash_result[:8],
        16
    )


    # 0 - 1 random value

    roll = number / 4294967295



    # House edge
    edge = 0.96



    # Casino style limbo curve
    multiplier = edge / (roll + 0.01)



    # minimum

    if multiplier < 1:
        multiplier = 1



    # maximum

    if multiplier > 100:
        multiplier = 100



    return round(
        multiplier,
        2
    )
