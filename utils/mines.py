import hashlib
import hmac



def generate_mines(
    server_seed,
    client_seed,
    nonce,
    total_cells=25,
    mine_count=3
):

    """
    Provably fair mine positions generator.

    Board:
    5x5 = 25 cells

    Returns:
    list of mine indexes
    """

    message = (
        f"{client_seed}:{nonce}:mines"
    )


    hash_result = hmac.new(
        server_seed.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()



    mines = []

    cursor = 0


    while len(mines) < mine_count:

        chunk = hash_result[
            cursor:cursor+8
        ]


        if len(chunk) < 8:

            hash_result = hashlib.sha256(
                hash_result.encode()
            ).hexdigest()

            cursor = 0
            continue



        number = int(
            chunk,
            16
        )


        position = number % total_cells


        if position not in mines:

            mines.append(
                position
            )


        cursor += 8


        if cursor >= len(hash_result):

            hash_result = hashlib.sha256(
                hash_result.encode()
            ).hexdigest()

            cursor = 0


    return mines
