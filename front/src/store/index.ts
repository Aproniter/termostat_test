import { combineReducers, configureStore } from '@reduxjs/toolkit'
import deviceReducer from './slices/deviceSlice'
import authReducer from './slices/authSlice'

const rootReducer = combineReducers({
    device: deviceReducer,
    auth: authReducer,
})


export function setupStore() {
    return configureStore({
        reducer: rootReducer
    })
}

export type RootState = ReturnType<typeof rootReducer>
export type AppStore = ReturnType<typeof setupStore>
export type AppDispatch = AppStore['dispatch']