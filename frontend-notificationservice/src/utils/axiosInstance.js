import axios from 'axios';

const axiosInstance = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
    // Add other headers as needed
  },
  withCredentials: true, // To include cookies in requests
});

export default axiosInstance;
