import { createSlice, PayloadAction } from '@reduxjs/toolkit'

interface AuthState {
    token: string
    isAuth: boolean
    error?: string
}

interface AuthPayload {
    token: string
    error?: string
}

const initialState: AuthState = {
    token: sessionStorage.getItem('at') ?? '',
    isAuth: Boolean(sessionStorage.getItem('at')),
    error: '',
}

export const authSlice = createSlice({
    name: 'auth',
    initialState,
    reducers: {
        signin(state, action: PayloadAction<AuthPayload>){
            state.token = action.payload.token
            state.isAuth = Boolean(action.payload.token)
            state.error = action.payload.error
            sessionStorage.setItem('at', action.payload.token)
        },
        signout(state){
            state.token = ''
            state.error = ''
            state.isAuth = false
            sessionStorage.removeItem('at')
            sessionStorage.removeItem('role')
        }
    }
})

export default authSlice.reducer