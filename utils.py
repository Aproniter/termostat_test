import hashlib
import random
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import and_

import models, schemas, capabilities, properties
from db import database
from exceptions import SendToDeviceException


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth')


def serial_number():
    return str(random.randint(10000000, 99999999))


def hash_password(password: str):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def validate_password(password: str, hashed_password: str):
    return hash_password(password) == hashed_password


async def send_command_to_device(device):
    query = (
                models.devices.update()
                .values(**{
                    i['state']['instance']: i['state']['value'] 
                    for i in device['capabilities']
                })
                .where(models.devices.c.id == device['id'])
            )
    await database.execute(query)


async def convert_to_yandex(data: list[schemas.Device], response_by_action: bool = False):
    """Конвертация данных из базы в формат Yandex Smart Home"""
    devices_to_response = [
        {
            'id': i['id'] if 'id' in i else i.id,
            'name': 'termostat_test',
            'type': 'devices.types.thermostat',
            'custom_data': {**i},
            'capabilities':[
                capabilities.thermostat_mode,
                capabilities.temperature_range,
                capabilities.brightness_range,
                capabilities.controls_locked_toggle,
                capabilities.on_off
            ]  if not response_by_action else i['capabilities'],
                "properties": [
                    properties.temperature_propertie
            ]
        } for i in data
    ]
    return devices_to_response


async def command_from_yandex(devices):
    """Парсинг запроса и выполнения команд от Yandex Smart Home"""
    for device in devices:
        try:
            send_command_to_device(device)
            for i in device['capabilities']:
                i['state'] = {
                    'instance': i['state']['instance'],
                    "action_result": {
                        "status": "DONE"
                    }
                }
        except SendToDeviceException:
            for i in device['capabilities']:
                i['state'] = {
                    'instance': i['state']['instance'],
                    "action_result": {
                        "status": "ERROR",
                        "error_code": "INVALID_ACTION",
                        "error_message": "the human readable error message"
                    }
                }
    return devices


async def create_user_token(user_id: int):
    query = (
        models.tokens.select().where(
        and_(
            models.tokens.c.user_id == user_id,
            models.tokens.c.expires > datetime.now()
        )
        )
    )
    token = await database.fetch_one(query)
    if token:
        return {'access_token': token.token, 'token_type': 'bearer', 'expires': token.expires}
    token = hashlib.sha256(
        str(random.randint(1000000, 9999999)).encode('utf-8')
    ).hexdigest()
    expires=datetime.now() + timedelta(weeks=2)
    query = (
        models.tokens.insert()
        .values(
            token=token,
            expires=expires, 
            user_id=user_id
        )
        # .returning(models.tokens.c.token, models.tokens.c.expires)
    )
    await database.execute(query)
    return {'access_token': token, 'token_type': 'bearer', 'expires': expires}


async def get_user_by_email(email: str):
    query = models.users.select().where(models.users.c.email == email)
    return await database.fetch_one(query)


async def get_user_by_token(token: str):
    query = models.tokens.join(models.users).select().where(
        and_(
            models.tokens.c.token == token,
            models.tokens.c.expires > datetime.now()
        )
    )
    return await database.fetch_one(query)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = await get_user_by_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid authentication credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    return user


async def create_user(email: str, password: str):
    query = models.users.insert().values(email=email, password=hash_password(password))
    db_user_id = await database.execute(query)
    token = await create_user_token(db_user_id)
    token_dict = {'access_token': token['access_token'], 'expires': token['expires']}
    return (db_user_id, token_dict)


async def delete_token_by_user(user_id: int):
    query = models.tokens.delete().where(models.tokens.c.user_id == user_id)
    return await database.execute(query)


async def create_device_for_user(user_id: int, device: dict):
    sn = serial_number()
    device['serial_number'] = sn
    device['owner_id'] = user_id
    query = models.devices.insert().values(**device)
    db_id = await database.execute(query)
    return (sn, db_id)


async def edit_device_for_user(device: dict):
    device_id = device.pop('id')
    device.pop('temp')
    query = models.devices.update().values(**device).where(models.devices.c.id == device_id)
    await database.execute(query)


async def get_all_user_devices(user_id: int):
    query = models.devices.select().where(models.devices.c.owner_id == user_id)
    return await database.fetch_all(query)


async def get_device_by_id(device_id: int):
    query = models.devices.select().where(models.devices.c.id == device_id)
    return await database.fetch_one(query)
