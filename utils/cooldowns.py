import time


cooldowns = {}



def check_cooldown(
    user_id,
    command,
    cooldown
):

    key = (
        user_id,
        command
    )


    current = time.time()


    if key not in cooldowns:

        cooldowns[key] = current

        return True, 0



    remaining = (
        cooldown
        -
        (current - cooldowns[key])
    )


    if remaining <= 0:

        cooldowns[key] = current

        return True, 0



    return False, int(remaining)



def reset_cooldown(
    user_id,
    command
):

    key = (
        user_id,
        command
    )


    if key in cooldowns:

        del cooldowns[key]



def get_remaining(
    user_id,
    command
):

    return cooldowns.get(
        (user_id, command),
        0
    )
