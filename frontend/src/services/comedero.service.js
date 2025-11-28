import api from "../api/api";
import { esAdminEnTambo } from "./tambo.service";

export const getInfoComedero = async (id) => {
    try {
      const comederoRes = await api.get(`/comederos/${id}`);
      return comederoRes.data;
    } catch (err) {
      const errMsg = err.response?.data?.detail || "Ocurrió un error inesperado";
      throw new Error(errMsg)
    }
}

export const EditComedero = async (id, comederoData) => {
  try {
    const res = await api.put(`/comederos/${id}`, comederoData);
    return res.data;
  } catch (err) {
    const errMsg = err.response?.data?.detail || "Ocurrió un error inesperado";
    throw new Error(errMsg);
  }
};

export const esAdminEnComedero = async (id) => {
    try{
      const comederoRes = await getInfoComedero(id);
      const es_admin = await esAdminEnTambo(comederoRes.id_tambo);
      return es_admin;
    } catch (err) {
      const errMsg = err.response?.data?.detail || "Ocurrió un error inesperado";
      throw new Error(errMsg)
    }
};

export const getComederoDetail = async (id) => {
  let comederoData = null;
  let dispositivosData = null;

  // Lógica para obtener el comedero
  try {
    const res = await getInfoComedero(id);
    comederoData = res;
  } catch (err) {
    console.error("Error al obtener detalles del comedero:", err);
  }

  try {
    const res = await api.get(`/dispositivos/${id}/comedero`);
    dispositivosData = res.data;
  } catch (err) {
    console.error("Error al obtener los dispositivos:", err);
  }

  if (comederoData) {
    return {
      ...comederoData,
      dispositivos: dispositivosData || [],
    }
  } else {
    throw new Error("No se pudo cargar la información del comedero.");
  }
};

export const addDeviceToComedero = async (comederoId, nombre) => {
  try{
    const device = {
      nombre: nombre,
      id_comedero: comederoId
    }
    const res = await api.post("/dispositivos/",
      device,
    );

    return res.data;
  } catch (err) {
      const errMsg = err.response?.data?.detail || "Ocurrió un error inesperado";
      throw new Error(errMsg)
  }
};
