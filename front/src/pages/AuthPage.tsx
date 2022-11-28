import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAppDispatch, useAppSelector } from "../hooks/redux";
import { signin } from "../store/actions/authActions";

export function AuthPage(){
    const isAuth = useAppSelector(state => state.auth.isAuth)
    const [errorMessage, setErrorMessage] = useState('')
    const [username_value, setUsername] = useState('')
    const [password_value, setPassword] = useState('')
    const [signup, setSignup] = useState(false)
    const dispatch = useAppDispatch()
    const navigate = useNavigate();
    const isFormValid = () => username_value && password_value

    const signupHendler = (status:boolean) => {
        setSignup(status)
        setUsername('');
        setPassword('');
    }

    const submitHandler = async (event: React.FormEvent) => {
        event.preventDefault()
        if (isFormValid()){
            try{
                await dispatch(signin({
                    username: username_value, 
                    password: password_value,
                }))
                navigate('/', { replace: false });
            } catch (e:any){
                if(e.response.data.detail){
                    setErrorMessage(e.response.data.detail)
                } else if(e.response.data.username){
                    setErrorMessage(e.response.data.username)
                }else if(e.response.data.errors){
                    setErrorMessage(e.response.data.errors)
                } else{
                    setErrorMessage(e.response.data)
                }
            }
        } else {
            alert('Заполните данные')
        }

    }

    if(isAuth){
        navigate('/', { replace: false });
    }

    return(
        <>
        {errorMessage && 
        <div className="container">
            {errorMessage}
        </div>
        }
        <div className="container">
            <span>
                <span>Войдите</span>
            </span>
            {(!signup &&
                <form className="login_form" onSubmit={submitHandler}>
                    <input 
                        className="login_usrname" 
                        type="text"
                        placeholder="Username"
                        value={username_value}
                        onChange={event => setUsername(event.target.value)}
                    ></input>
                    <input 
                        className="login_password" 
                        type="password"
                        placeholder="Пароль"
                        value={password_value}
                        onChange={event => setPassword(event.target.value)}
                    ></input>
                    <button className="login" type="submit">Войти</button>
                </form>)
            }
        </div>
        </>
    )
}