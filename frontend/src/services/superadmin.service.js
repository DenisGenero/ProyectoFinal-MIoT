// src/services/superadmin.service.js
import api from "../api/api";

// traer todos los dispositivos
export const getAllDevices = async () => {
  const res = await api.get("/dispositivos");
  return res.data;
};

// traer solo los no configurados
export const getUnconfiguredDevices = async () => {
  const res = await api.get("/dispositivos/sin-config");
  return res.data;
};

// filtrar por tambo
export const getDevicesByTambo = async (tamboId) => {
  const res = await api.get(`/superadmin/dispositivos/tambo/${tamboId}`);
  return res.data;
};

// filtrar por comedero
export const getDevicesByComedero = async (comederoId) => {
  const res = await api.get(`/superadmin/dispositivos/comedero/${comederoId}`);
  return res.data;
};

// filtrar por usuario
export const getDevicesByUser = async (userId) => {
  const res = await api.get(`/superadmin/dispositivos/usuario/${userId}`);
  return res.data;
};


// ----- USUARIOS -----

// buscar usuario por mail
export const findUserByEmail = async (email) => {
  const res = await api.get(`/superadmin/usuarios?email=${email}`);
  return res.data;
};

// convertir un usuario en superusuario
export const promoteToSuperuser = async (userId) => {
  const res = await api.post(`/superadmin/usuarios/${userId}/promover`);
  return res.data;
};

export const getDevicesByMac = async (mac) => {
  const res = await api.get(`/dispositivos/mac`,{
    params: {
      mac_address: mac
    }
  });
  return res.data;
};

export const getDevicesByUserEmail = async (email) => {
  try{
    const res = await api.get(`/dispositivos/usuario`, {
      params: {
        email: email
      }
    });
    return res.data;
  } catch (error){
    console.error("Error al obtener dispositivos por email:", error);
    return [];
  }
};

export async function updateDeviceAdminConfig(deviceId, body) {
  const res = await api.put(`/dispositivos/${deviceId}/admin-config`, body);
  return res.data;
}