from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Boolean, Numeric, BigInteger, ForeignKey, UniqueConstraint
from decimal import Decimal

class Base(DeclarativeBase):
    pass


class Kwork(Base):
    __tablename__ = 'kworks'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[str] = mapped_column(String(3000))
    is_new: Mapped[bool] = mapped_column(Boolean, default=True)
    kwork_count: Mapped[int] = mapped_column(Integer, default=0)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=True)
    url: Mapped[str] = mapped_column(String(500))
    users: Mapped[list['UserKwork']] = relationship(back_populates='kwork', cascade="all, delete-orphan")


#
class User(Base):
    __tablename__ = 'users'


    telegram_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True, index=True)
    viewed_all: Mapped[bool] = mapped_column(Boolean, default=False)
    kworks: Mapped[list['UserKwork']] = relationship(back_populates='user', cascade="all, delete-orphan")


class UserKwork(Base):
    __tablename__ = 'user_kworks'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.telegram_id'))
    kwork_id: Mapped[int] = mapped_column((ForeignKey('kworks.id')))
    viewed: Mapped[bool] = mapped_column(Boolean, default=False)

    user: Mapped[User] = relationship(back_populates='kworks')
    kwork: Mapped[Kwork] = relationship(back_populates='users')

    __table_args__ = (
        UniqueConstraint("user_id", "kwork_id", name="uq_user_kwork"),
    )