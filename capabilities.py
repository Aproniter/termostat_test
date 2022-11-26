thermostat_mode = {
    "type": "devices.capabilities.mode",
    "retrievable": True,
    "parameters": {
        "instance": "thermostat",
        "modes": [
            {
            "value": "cool"
            },
            {
            "value": "heat"
            }
        ]
    }
}


temperature_range = {
    "type": "devices.capabilities.range",
    "retrievable": True,
    "parameters": {
        "instance": "temperature",
        "random_access": True,
        "range": {
            "max": 40,
            "min": 18,
            "precision": 1
        },
        "unit": "unit.temperature.celsius"
    }
}


brightness_range = {
    "type": "devices.capabilities.range",
    "retrievable": True,
    "parameters": {
        "instance": "brightness",
        "random_access": True,
        "range": {
            "max": 100,
            "min": 1,
            "precision": 1
        },
        "unit": "unit.percent"
    }
}


controls_locked_toggle = {
    "type": "devices.capabilities.toggle",
    "retrievable": True,
    "parameters": {
        "instance": "controls_locked"
    }
}


on_off = {
    "type": "devices.capabilities.on_off",
    "retrievable": True
}
