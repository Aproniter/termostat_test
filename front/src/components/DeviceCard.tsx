import { IDevice } from "../models"
import { useState } from "react";
import { useNavigate } from'react-router-dom'
import instance from '../axios' 

interface DeviceCardProps {
    device: IDevice
}

export function DeviceCard({ device }:DeviceCardProps) {
    const navigate = useNavigate()
    const [temperature, setTemperature] = useState(String(device.temperature))
    const [brightness, setBrightness] = useState(String(device.brightness))
    const [wifiChecked, setWifiChecked] = useState(device.status_wifi);
    const [controlsLockedChecked, setControlsLockedChecked] = useState(device.controls_locked);
    const [thermostatValue, setThermostatValue] = useState(device.thermostat);

    function checkboxWifiHandler () {
        setWifiChecked(prev => !prev);
    }

    function checkboxLockedHandler () {
        setControlsLockedChecked(prev => !prev);
    }

    function chengeSelect(e:any) {
        setThermostatValue(e.target.value);
    }

    const deviceStateClickHandler = async (event: React.FormEvent) => {
        event.preventDefault()
        await instance.post(
            '/devices/edit_stat/', {
                "id": device.id,
                "on": device.on,
                "status_wifi": wifiChecked,
                "temp": device.temp ? device.temp : 0,
                "temperature": temperature,
                "brightness": brightness,
                "thermostat": thermostatValue,
                "controls_locked": controlsLockedChecked
            },{
                headers: {
                    'Authorization': `Bearer ${sessionStorage.getItem('at')}`
                }
                }
        )
        navigate('/');

    }

    return(
        <div 
            className="card"
            // onClick={deviceCardClickHandler}
        >
            <form className="login_form" onSubmit={deviceStateClickHandler}>
                <p className="card-title">{device.serial_number}</p>
                <label>wifi</label>
                <input 
                    className="card-status_wifi" 
                    type="checkbox"
                    onChange={checkboxWifiHandler} 
                    checked={wifiChecked}
                ></input>
                <p className="card-temp">Текущая температура: {device.temp}</p>
                <label>Установить температуру</label>
                <input 
                    className="card-temperature" 
                    type="number"
                    value={temperature}
                    onChange={event => setTemperature(event.target.value)}
                ></input>
                <p className="card-brightness">Яркость: {device.brightness}</p>
                <label>Установить яркость</label>
                <input 
                    className="card-brightness-input" 
                    type="number"
                    value={brightness}
                    onChange={event => setBrightness(event.target.value)}
                ></input><br></br>
                <select value={thermostatValue} onChange={chengeSelect}>
                    <option value="cool">Охлаждение</option>
                    <option value="heat">Нагрев</option>
                </select><br></br>
                <label>Блокировка кнопок</label>
                <input 
                    className="card-controls_locked" 
                    type="checkbox"
                    onChange={checkboxLockedHandler} 
                    checked={controlsLockedChecked}
                ></input><br></br>
                <button className="send-state-to-device" type="submit">Обновить на устройстве</button>
            </form>
        </div>
    )
}