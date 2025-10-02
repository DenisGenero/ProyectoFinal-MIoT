import axios from "axios";
import { logout } from "../services/auth.service";

const api = axios.create({
  baseURL: "http://localhost:8000/api",
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
    (error) => {
      if (error.response && error.response.status === 401) {
        //localStorage.removeItem("token");
        logout()
      }
return Promise.reject(error); // Rechaza la promesa para que el error pueda ser capturado
}
);

export default api;
