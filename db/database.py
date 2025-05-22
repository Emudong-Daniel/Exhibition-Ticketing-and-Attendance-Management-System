from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime

Base = declarative_base()

class Guest(Base):
    __tablename__ = 'guests'
    guest_id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    title = Column(String)
    affiliation = Column(String)

class Event(Base):
    __tablename__ = 'events'
    event_id = Column(Integer, primary_key=True)
    title = Column(String)
    type = Column(String)

class Session(Base):
    __tablename__ = 'sessions'
    session_id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('events.event_id'))
    session_type = Column(String)
    time_slot = Column(String)
    date = Column(Date)
    event = relationship("Event", back_populates="sessions")

Event.sessions = relationship("Session", order_by=Session.session_id, back_populates="event")

class Seat(Base):
    __tablename__ = 'seats'
    seat_id = Column(Integer, primary_key=True)
    category = Column(String)
    price = Column(Float)
    seat_number = Column(String)
    status = Column(String)

class Reservation(Base):
    __tablename__ = 'reservations'
    reservation_id = Column(Integer, primary_key=True)
    guest_id = Column(Integer, ForeignKey('guests.guest_id'))
    session_id = Column(Integer, ForeignKey('sessions.session_id'))
    seat_id = Column(Integer, ForeignKey('seats.seat_id'))
    booking_time = Column(DateTime, default=datetime.datetime.utcnow)
    ticket_id = Column(String)

# SQLite engine and session creation
engine = create_engine('sqlite:///exhibition.db')
Base.metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine)
