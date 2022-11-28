import axios from 'axios'
import { AppDispatch } from '../index'
import { authSlice } from '../slices/authSlice';

const baseUrl = 'http://127.0.0.1:8000/'


interface AuthResponse {
    token: string
    detail?: string
    user: {
        email: string
        first_name: string
        id: number
        last_name: string
        username: string
    }

}

interface AuthData {
    username: string
    password: string
}

export const signin = (data: AuthData) => {
    return async (dispatch: AppDispatch) => {
        try {
            let response
            // if(data.first_name && data.last_name){
            //     response = await axios.post<AuthResponse>(baseUrl+'auth/', data);
            // } else {
            //     response = await axios.post<AuthResponse>(baseUrl+'auth/', data);
            // }
            response = await axios.post(baseUrl+'auth', {
                "username": data.username, "password": data.password, "grant_type": "password"
            }, {
                headers: {
                  'content-type': 'application/x-www-form-urlencoded'
                }
              });
            console.log(response.data)
            dispatch(authSlice.actions.signin({
                token: response.data.access_token,
                error: response.data.detail
            }))
        } catch (e) {
            throw e;
        }
    }
}