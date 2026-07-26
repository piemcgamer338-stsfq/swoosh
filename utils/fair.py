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

    number = int(
        hash_result[:8],
        16
    )

    return number


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

import hashlib


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
    ) % 100 + 1


    return number
