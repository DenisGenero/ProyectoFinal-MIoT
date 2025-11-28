// src/services/auth.service.js
import api from "../api/api";

// LOGIN
export const login = async (email, password) => {
  const params = new URLSearchParams();
  params.append("username", email);
  params.append("password", password);

  try {
    const res = await api.post("/auth/login", params, {
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
    });

    return res.data;
  } catch (err) {
    const errMsg = err.response?.data?.detail || "Ocurrió un error inesperado";
    throw new Error(errMsg)
  }
};

// REGISTER
export const register = async (nombre, apellido, email, password) => {
  try{
    const res = await api.post("/auth/register", {
      nombres: nombre,
      apellidos: apellido,
      email,
      password,
    });

    return res.data;
  } catch (err) {
    const errMsg = err.response?.data?.detail || "Ocurrió un error inesperado";
    throw new Error(errMsg)
  }
};

// LOGOUT (sin endpoint, solo limpia localStorage)
export const logout = () => {
  localStorage.removeItem("token");
  localStorage.removeItem("user");
};

// ME (opcional)
export const me = async () => {
  const res = await api.get("/auth/me");

  return res.data;
};

export async function getUserInfo() {
  try {
    const res = await api.get("/usuarios/me");
    return res.data;
  } catch (err) {
    const msg = err.response?.data?.detail || "Error al obtener usuario";
    throw new Error(msg);
  }
}


export async function actualizarUsuario(data) {
  console.log(data)
  try {
    const res = await api.put("/usuarios/actualiza_mismo_usuario", data);
    return res.data;
  } catch (err) {
    const msg = err.response?.data?.detail || "Error al actualizar usuario";
    throw new Error(msg);
  }
}



