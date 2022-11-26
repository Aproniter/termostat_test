from datetime import datetime
from pydantic import BaseModel

from models import DeviceMode


class DeviceBase(BaseModel):
    on: bool = False
    status_wifi: bool = True
    temp: float = 0.0
    temperature: int = 0
    brightness: int = 100
    thermostat: DeviceMode
    controls_locked: bool = False


class DeviceCreate(DeviceBase):
    pass


class DeviceEdit(DeviceBase):
    id: int


class Device(DeviceBase):
    id: int
    serial_number: int
    owner_id: int

    class Config:
        orm_mode = True


class DeviceToYandex(BaseModel):
    id: str
    name: str | None
    type: str | None
    custom_data: dict | None
    capabilities: list[dict] | None
    properties: list[dict] | None


class Payload(BaseModel):
    devices: list[DeviceToYandex]


class PayloadResponse(Payload):
    user_id: str
    devices: list[DeviceToYandex]


class ResponseFromYandex(BaseModel):
    payload: Payload


class ResponseToYandex(BaseModel):
    request_id: str
    payload: PayloadResponse


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class Token(BaseModel):
    access_token: str
    expires: datetime
    token_type: str | None = 'bearer'

    class Config:
        allow_population_by_field_name = True


class User(UserBase):
    id: int
    devices: tuple[DeviceBase] = ()
    token: Token = {}

    class Config:
        orm_mode = True
