import asyncio

from services.economy import (
    add_balance,
    remove_balance
)


ACTIVE_RAIN = None


class Rain:

    def __init__(
        self,
        host_id,
        amount,
        duration,
        channel,
        message
    ):

        self.host_id = host_id

        self.amount = amount

        self.duration = duration

        self.channel = channel

        self.message = message

        self.participants = set()

        self.finished = False



    def join(
        self,
        user_id
    ):

        if self.finished:
            return False

        if user_id == self.host_id:
            return False

        if user_id in self.participants:
            return False

        self.participants.add(
            user_id
        )

        return True



    async def finish(self):

        self.finished = True


        if len(
            self.participants
        ) == 0:

            await add_balance(
                self.host_id,
                self.amount
            )

            return {
                "refund": True,
                "each": 0,
                "count": 0
            }


        each = (
            self.amount /
            len(self.participants)
        )


        for user in self.participants:

            await add_balance(
                user,
                each
            )


        return {
            "refund": False,
            "each": each,
            "count": len(
                self.participants
            )
        }



async def create_rain(
    host_id,
    amount,
    duration,
    channel,
    message
):

    global ACTIVE_RAIN


    if ACTIVE_RAIN:

        return None


    await remove_balance(
        host_id,
        amount
    )


    ACTIVE_RAIN = Rain(
        host_id,
        amount,
        duration,
        channel,
        message
    )


    asyncio.create_task(
        rain_task()
    )


    return ACTIVE_RAIN



async def rain_task():

    global ACTIVE_RAIN


    rain = ACTIVE_RAIN


    await asyncio.sleep(
        rain.duration
    )


    await rain.finish()


    ACTIVE_RAIN = None
