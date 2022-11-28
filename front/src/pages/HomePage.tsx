import { useEffect, useState } from "react";
import { fetchDevices } from "../store/actions/deviceActions";
import { useAppDispatch, useAppSelector } from "../hooks/redux";
import { Link, useNavigate } from "react-router-dom";
import { Downloading } from "../components/Downloading"
import { DeviceCard } from "../components/DeviceCard";



export function HomePage(){
    const isAuth = useAppSelector(state => state.auth.isAuth)
    const navigate = useNavigate();
    const dispatch = useAppDispatch()
    const {error, loading, total_count, devices} = useAppSelector(state => state.device)

    useEffect(() => {
        if(!isAuth){
          navigate('/auth', { replace: false });
        }
      }, [isAuth, navigate]);

    useEffect(() => {
        dispatch(fetchDevices())
    }, [dispatch])


    return(
        <div className="container">
            {loading && <Downloading/>}
            {error && <p className="error-block">{error}</p>}
            <div className="devices">
                {devices.map(
                        device => 
                        <DeviceCard key={device.id} device={device}/>
                )}
            </div>
        </div>
    )
}