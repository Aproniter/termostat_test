import uvicorn
import random
from typing import List
from fastapi import FastAPI
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

import models, schemas, utils

from db import database, metadata, engine


app = FastAPI()


metadata.create_all(engine)


@app.on_event('startup')
async def startup():
    await database.connect()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()


@app.post('/auth', response_model=schemas.Token)
async def auth(form_data: OAuth2PasswordRequestForm = Depends()):
    """Аутентификация пользователя"""
    user = await utils.get_user_by_email(email=form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail='Проверьте email или пароль')
    if not utils.validate_password(
        password=form_data.password, hashed_password=user['password']
    ):
        raise HTTPException(status_code=400, detail='Проверьте email или пароль')
    return await utils.create_user_token(user_id=user['id'])


@app.get("/users/me", response_model=schemas.UserBase)
async def read_users_me(current_user: schemas.User = Depends(utils.get_current_user)):
    """Вернуть текущего пользователя"""
    return current_user


@app.post('/users/', response_model=schemas.User)
async def create_user(user: schemas.UserCreate):
    """Создать пользователя"""
    db_id, token_dict = await utils.create_user(user.email, user.password)
    return {**user.dict(), 'id': db_id, 'token': token_dict}


@app.get('/users/{user_id}', response_model=schemas.User)
async def get_user_by_id(user_id: int):
    """Получить пользователя по id"""
    query = models.users.select().where(models.users.c.id == user_id)
    return await database.fetch_one(query)


@app.get('/users/', response_model=List[schemas.User])
async def get_all_users(offset: int = 0, limit: int = 10):
    """Получить список пользователей"""
    query = models.users.select().offset(offset).limit(limit)
    return await database.fetch_all(query)


@app.post('/users/devices/', response_model=schemas.Device)
async def create_device_for_user(device: schemas.DeviceCreate, current_user: schemas.User = Depends(utils.get_current_user)):
    """Создать устройство для текущего пользователя"""
    device = device.dict()
    sn, db_id = await utils.create_device_for_user(current_user.id, device)
    return {**device, 'id': db_id, 'owner_id': current_user.id, 'serial_number': sn}


@app.get('/users/devices/', response_model=List[schemas.Device])
async def get_all_user_devices(current_user: schemas.User = Depends(utils.get_current_user)):
    """Получить все устройства текущего пользователя"""
    return await utils.get_all_user_devices(current_user.id)


@app.get('/v1.0/user/devices', response_model=schemas.ResponseToYandex)
async def get_all_user_devices_to_yandex(current_user: schemas.User = Depends(utils.get_current_user)):
    """Получить все устройства текущего пользователя для Yandex Smart Home"""
    devices = await utils.get_all_user_devices(current_user.id)
    response = {
        'request_id': str(random.randint(10000000, 99999999)),
        'payload': {
            'user_id': str(current_user.id),
            'devices': await utils.convert_to_yandex(devices)
        }
    }
    return response


@app.post('/v1.0/user/devices/action', response_model=schemas.ResponseToYandex)
async def edit_user_devices_state_from_yandex(
    payload: schemas.ResponseFromYandex,
    current_user: schemas.User = Depends(utils.get_current_user),
):
    """Изменить состояние устройства текущего пользователя из Yandex Smart Home"""
    devices = await utils.command_from_yandex(payload.dict()['payload']['devices'])
    response = {
        'request_id': str(random.randint(10000000, 99999999)),
        'payload': {
            'user_id': str(current_user.id),
            'devices': await utils.convert_to_yandex(devices, response_by_action=True)
        }
    }
    return response


@app.post('/users/devices/edit_stat/', response_model=schemas.DeviceEdit)
async def edit_stat_device_for_user(device: schemas.DeviceEdit, current_user: schemas.User = Depends(utils.get_current_user)):
    """Изменить настройки устройства"""
    device = device.dict()
    await utils.edit_device_for_user(device.copy())
    return {**device}


@app.get('/devices/{device_id}', response_model=schemas.Device)
async def get_device_by_id(device_id: int):
    """Получить устройство по id"""
    return await utils.get_device_by_id(device_id)


@app.head('/v1.0/')
async def smart_home_unlink():
    """Проверка доступности Endpoint URL"""
    return status.HTTP_200_OK


@app.post('/v1.0/user/unlink')
async def delete_token_by_user(current_user: schemas.User = Depends(utils.get_current_user)):
    """Оповещение о разъединении аккаунтов"""
    status = await utils.delete_token_by_user(current_user.id)
    if status:
        return {"request_id": str(random.randint(10000000, 99999999))}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
