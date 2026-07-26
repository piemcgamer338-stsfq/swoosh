from utils.constants import RANK_REQUIREMENTS


def get_rank(total_wager: float):

    current = "Bronze"
    next_rank = None

    ranks = list(RANK_REQUIREMENTS.items())

    for i, (name, wager) in enumerate(ranks):

        if total_wager >= wager:
            current = name

            if i + 1 < len(ranks):
                next_rank = ranks[i + 1][0]

    return current, next_rank


def progress(total_wager):

    ranks = list(RANK_REQUIREMENTS.items())

    current = ranks[0]
    nxt = None

    for i in range(len(ranks)):

        if total_wager >= ranks[i][1]:

            current = ranks[i]

            if i + 1 < len(ranks):
                nxt = ranks[i + 1]

    if nxt is None:
        return 100

    current_req = current[1]
    next_req = nxt[1]

    return (
        (total_wager-current_req)
        /
        (next_req-current_req)
    ) * 100
