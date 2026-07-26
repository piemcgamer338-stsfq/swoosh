import hashlib
import secrets
import hmac



def generate_server_seed():

    return secrets.token_hex(32)




def hash_server_seed(
    server_seed
):

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
    nonce,
    game
):

    message = (
        f"{client_seed}:{nonce}:{game}"
    )


    result = hmac.new(
        server_seed.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()


    return result




def number_from_hash(
    hash_result
):

    return int(
        hash_result[:8],
        16
    )




# ==========================
# COINFLIP
# ==========================


def coinflip_result(
    server_seed,
    client_seed,
    nonce
):

    hash_result = generate_result(
        server_seed,
        client_seed,
        nonce,
        "coinflip"
    )


    number = number_from_hash(
        hash_result
    )


    if number % 2 == 0:

        return "heads"


    return "tails"





# ==========================
# DICE
# ==========================


def dice_result(
    server_seed,
    client_seed,
    nonce
):

    hash_result = generate_result(
        server_seed,
        client_seed,
        nonce,
        "dice"
    )


    number = (
        number_from_hash(hash_result)
        % 100
    ) + 1


    return number





# ==========================
# LIMBO
# ==========================


def limbo_result(
    server_seed,
    client_seed,
    nonce
):

    hash_result = generate_result(
        server_seed,
        client_seed,
        nonce,
        "limbo"
    )


    number = number_from_hash(
        hash_result
    )


    # 1.00x - 100.00x
    result = (
        1 +
        (number % 9900) / 100
    )


    return round(
        result,
        2
    )





# ==========================
# MINES
# ==========================


def mines_result(
    server_seed,
    client_seed,
    nonce,
    total_cells=25,
    mine_count=3
):


    hash_result = generate_result(
        server_seed,
        client_seed,
        nonce,
        "mines"
    )


    mines = []


    cursor = 0



    while len(mines) < mine_count:


        if cursor + 8 > len(hash_result):


            hash_result = hashlib.sha256(
                hash_result.encode()
            ).hexdigest()


            cursor = 0



        chunk = hash_result[
            cursor:cursor+8
        ]


        number = int(
            chunk,
            16
        )


        position = (
            number %
            total_cells
        )


        if position not in mines:

            mines.append(
                position
            )


        cursor += 8



    return mines
