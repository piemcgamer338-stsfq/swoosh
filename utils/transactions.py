import secrets
from datetime import datetime



def generate_tx_id():

    return (
        secrets.token_hex(8)
    )



def transaction_status(status):

    statuses = {

        "Pending": "⏳ Pending",

        "Confirmed": "✅ Confirmed",

        "Completed": "🟢 Completed",

        "Rejected": "❌ Rejected"

    }


    return statuses.get(
        status,
        "❓ Unknown"
    )



def transaction_time():

    return datetime.utcnow()



def create_transaction(
    user_id,
    amount,
    address
):

    return {

        "id": generate_tx_id(),

        "user": user_id,

        "amount": amount,

        "address": address,

        "status": "Pending",

        "time": transaction_time()

    }
