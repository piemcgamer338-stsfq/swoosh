from datetime import datetime



def log(message):

    print(
        f"[{datetime.utcnow()}] {message}"
    )



def error(message):

    print(
        f"[ERROR {datetime.utcnow()}] {message}"
    )



def success(message):

    print(
        f"[SUCCESS {datetime.utcnow()}] {message}"
    )
