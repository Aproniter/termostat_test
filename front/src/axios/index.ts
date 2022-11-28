import axios from 'axios'

const baseUrl = 'http://127.0.0.1:8000'

const instance = axios.create({
    // baseURL: process.env.REACT_APP_BASE_URL,
    baseURL: baseUrl
});

// const token = '';

// instance.defaults.headers.common['Authorization'] = `Token ${token}`;
instance.defaults.headers.common['Content-Type'] = 'application/json';

export default instance;