from sqlalchemy import (
    BigInteger,
    Boolean,
    Float,
    Integer,
    String,
    DateTime
)

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column
)

from datetime import datetime


class Base(DeclarativeBase):
    pass


class User(Base):

    __tablename__ = "users"

    discord_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True
    )

    username: Mapped[str] = mapped_column(
        String(100),
        default=""
    )

    balance: Mapped[float] = mapped_column(
        Float,
        default=0.0
    )

    vault: Mapped[float] = mapped_column(
        Float,
        default=0.0
    )

    wager: Mapped[float] = mapped_column(
        Float,
        default=0.0
    )

    weekly_wager: Mapped[float] = mapped_column(
        Float,
        default=0.0
    )

    total_deposit: Mapped[float] = mapped_column(
        Float,
        default=0.0
    )

    total_withdraw: Mapped[float] = mapped_column(
        Float,
        default=0.0
    )

    rakeback: Mapped[float] = mapped_column(
        Float,
        default=0.0
    )

    level: Mapped[int] = mapped_column(
        Integer,
        default=1
    )

    xp: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    affiliate_code: Mapped[str] = mapped_column(
        String(32),
        default=""
    )

    referred_by: Mapped[int | None] = mapped_column(
        BigInteger,
        nullable=True
    )

    daily_claim: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    weekly_claim: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    banned: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )
