import axios from 'axios';

const api = axios.create({
    baseURL: import.meta.API_GATEWAY_ADDRESS,
})

export default api;