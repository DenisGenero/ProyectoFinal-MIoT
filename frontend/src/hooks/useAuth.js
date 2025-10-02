// src/hooks/useAuth.js
import { useState } from "react";
import * as authService from "../services/auth.service";

export function useAuth() {
  const [user, setUser] = useState(
    JSON.parse(localStorage.getItem("user")) || null
  );

  const login = async (email, password) => {
    const data = await authService.login(email, password);
    localStorage.setItem("token", data.access_token);
    localStorage.setItem("user", JSON.stringify(data.user));
    setUser(data.user);
  };

  const register = async (nombre, apellido, email, password) => {
    await authService.register(nombre, apellido, email, password);
  };

  const logout = () => {
    authService.logout();
    setUser(null);
  };

  return { user, login, register, logout };
}
