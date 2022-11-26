import enum
from sqlalchemy import (
    Boolean, Column, DateTime, Enum, Float, 
    ForeignKey, Integer, String, Table
)

from db import metadata


class DeviceMode(enum.Enum):
    cool = 'cool'
    heat = 'heat'


users = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('email', String, unique=True, index=True),
    Column('password', String),
)

tokens = Table(
    'tokens',
    metadata,
    Column('id', Integer, primary_key=True),
    Column(
        'token',
        String,
        unique=True,
        nullable=False,
        index=True,
    ),
    Column('expires', DateTime()),
    Column('user_id', ForeignKey('users.id')),
)

devices = Table(
    'devices',
    metadata,
    Column(
        'id',
        Integer,
        primary_key=True,
        unique=True,
    ),
    Column(
        'serial_number',
        Integer,
        unique=True
    ),
    Column('on', Boolean, default=False),
    Column('status_wifi', Boolean, default=False),
    Column('temp', Float, default=0.0),
    Column('temperature', Integer, default=0),
    Column('brightness', Integer, default=100),
    Column('thermostat', Enum(DeviceMode), default=DeviceMode.cool),
    Column('controls_locked', Boolean, default=False),
    Column('owner_id', Integer, ForeignKey('users.id')),
)
