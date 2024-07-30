from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from sqlalchemy import String


class Base(DeclarativeBase):
    pass


class HistModel(Base):
    __tablename__ = "hist"

    date: Mapped[str] = mapped_column(String(30), primary_key=True)
    ticker: Mapped[str] = mapped_column(String(30), primary_key=True)
    close: Mapped[float] = mapped_column()
