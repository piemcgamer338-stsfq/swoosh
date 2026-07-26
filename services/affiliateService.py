async def get_affiliate(user):

    return {
        "owner": user.id,
        "referrals": 0,
        "earned": 0
    }


async def reward_affiliate(
    owner,
    wager
):

    reward = wager * 0.01

    return reward
