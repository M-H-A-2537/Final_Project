from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker, relationship

engine = create_engine('sqlite:///messenger.db')

class Base(DeclarativeBase) :
    pass
base = Base()

class User(Base):
    __tablename__ = "user"
    id : Mapped[int] = mapped_column(primary_key = True)
    username : Mapped[str] = mapped_column(unique = True)
    bio : Mapped[str] = mapped_column()
    phone : Mapped[str] = mapped_column(unique = True)
    password : Mapped[str] = mapped_column()
    profile_image : Mapped[str] = mapped_column()
    contacts : Mapped[list["Contact"]] = relationship("Contact", back_populates = "user")
    sent_messages: Mapped[list["Message"]] = relationship("Message", back_populates="sender", foreign_keys="Message.send_id")
    received_messages: Mapped[list["Message"]] = relationship("Message", back_populates="receiver", foreign_keys="Message.receive_id")

class Contact(Base) :
    __tablename__ = "contact"
    id : Mapped[int] = mapped_column(primary_key = True)
    username: Mapped[str] = mapped_column(unique=True)
    bio: Mapped[str] = mapped_column()
    phone: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()
    profile_image: Mapped[str] = mapped_column()
    user_id : Mapped[int] = mapped_column(ForeignKey("user.id"))
    user : Mapped["User"] = relationship("User", back_populates = "contacts")

class Message(Base) :
    __tablename__ = "message"
    id: Mapped[int] = mapped_column(primary_key=True)
    send_id : Mapped[int] = mapped_column(ForeignKey("user.id"))
    receive_id : Mapped[int] = mapped_column(ForeignKey("user.id"))
    message : Mapped[str] = mapped_column()
    sender: Mapped["User"] = relationship("User", back_populates="sent_messages", foreign_keys=[send_id])
    receiver: Mapped["User"] = relationship("User", back_populates="received_messages", foreign_keys=[receive_id])

base.metadata.create_all(engine)

SessionLocal = sessionmaker(bind = engine)
session = SessionLocal()
