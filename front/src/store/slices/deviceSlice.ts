import { IDevice } from "../../models"
import { createSlice, PayloadAction } from '@reduxjs/toolkit'

interface DeviceState {
    loading: boolean
    error: string
    devices: IDevice[]
    total_count: number
}

const initialState:DeviceState = {
    loading: false,
    error: '',
    devices: [],
    total_count: 0
}

interface DevicePayload {
    devices: IDevice[],
    total_count: number
}

export const deviceSlice = createSlice({
    name: 'device',
    initialState,
    reducers: {
        fetching(state) {
            state.loading = true
            state.error = ''
        },
        fetchingSuccess(state, action: PayloadAction<DevicePayload>) {
            state.loading = false
            state.devices = action.payload.devices
            state.total_count = action.payload.total_count
            state.error = ''
        },
        fetchError(state, action: PayloadAction<Error>){
            state.loading = false
            state.error = action.payload.message
        }
    }
})

export default deviceSlice.reducer