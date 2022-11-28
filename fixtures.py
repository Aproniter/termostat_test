import utils


async def create_test_data_to_db():
    for i in range(1,4):
        await utils.create_user(str(i), str(i))

    for i in range(1,4):
        device = {
            'on': False,
            'status_wifi': True,
            'temp': 0.0,
            'temperature': 0,
            'brightness': 100,
            'thermostat': 'cool',
            'controls_locked': False
        }
        for j in range(3):
            await utils.create_device_for_user(i, device)

if __name__ == '__main__':
    pass
