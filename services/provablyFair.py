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



def get_number(
    server_seed,
    client_seed,
    nonce,
    maximum
):

    result = generate_result(
        server_seed,
        client_seed,
        nonce
    )


    number = int(
        result[:8],
        16
    )


    return number % maximum



def verify(
    server_seed,
    client_seed,
    nonce,
    result
):

    generated = generate_result(
        server_seed,
        client_seed,
        nonce
    )

    return generated == result
