import hashlib



def generate_mines(
    server_seed,
    client_seed,
    nonce,
    total_cells=25,
    mine_count=3
):

    data = (
        f"{server_seed}:{client_seed}:{nonce}:mines"
    )


    hash_result = hashlib.sha256(
        data.encode()
    ).hexdigest()


    mines = []

    cursor = 0



    while len(mines) < mine_count:


        if cursor + 8 > len(hash_result):

            hash_result = hashlib.sha256(
                hash_result.encode()
            ).hexdigest()

            cursor = 0



        chunk = hash_result[
            cursor:cursor + 8
        ]


        number = int(
            chunk,
            16
        )


        position = (
            number % total_cells
        )


        if position not in mines:

            mines.append(
                position
            )


        cursor += 8



    return mines
