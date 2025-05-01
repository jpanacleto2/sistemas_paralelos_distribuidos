import axios from 'axios';

const api = axios.create({
    baseURL: 'http://192.177.111.130:8080',
})

export default api;