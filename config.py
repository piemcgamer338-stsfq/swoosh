import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

DATABASE_URL = os.getenv("DATABASE_URL")

OWNER_ID = int(os.getenv("OWNER_ID"))

PREFIX = os.getenv("PREFIX", ".")

LTC_XPUB = os.getenv("LTC_XPUB")

LTC_WALLET = os.getenv("LTC_WALLET")

SOL_WALLET = os.getenv("SOL_WALLET")

USDT_WALLET = os.getenv("USDT_WALLET")

POINT_VALUE_USD = 0.005

MIN_DEPOSIT_USD = 0.10

MIN_WITHDRAW_USD = 1.00

HOUSE_BALANCE = 80
