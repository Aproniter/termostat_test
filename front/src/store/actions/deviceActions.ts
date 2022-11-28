import { AppDispatch } from '..'
import instance from '../../axios' 
import { IDevice, ListServerResponse } from '../../models'
import { deviceSlice } from "../slices/deviceSlice"

export const fetchDevices = () => {
    return async(dispatch:AppDispatch) => {
        try {
            dispatch(deviceSlice.actions.fetching())
            const resp = await instance.get<ListServerResponse<IDevice[]>>(
                '/devices/', {
                    headers: {
                        'Authorization': `Bearer ${sessionStorage.getItem('at')}`
                    }
                  }
            )
            dispatch(deviceSlice.actions.fetchingSuccess({
                devices: resp.data.results.items,
                total_count: resp.data.total_count,
            }))
        } catch(e) {
            dispatch(deviceSlice.actions.fetchError(e as Error))
        }
    }
}