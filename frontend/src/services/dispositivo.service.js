import api from "../api/api";
import { esAdminEnComedero } from "./comedero.service";

// GET detalle dispositivo
export const getDispositivoDetail = async (id) => {
    try{
        const res = await api.get(`/dispositivos/${id}/config/`);
        return res.data;
    } catch (err) {
      const errMsg = err.response?.data?.detail || "Ocurrió un error inesperado";
      throw new Error(errMsg)
    }
};

export const updateDispositivoConfig = async (id, data) => {
  try{
    const res = await api.put(`/dispositivos/${id}/config`, data);
    return res.data;
  } catch (err) {
      const errMsg = err.response?.data?.detail || "Ocurrió un error inesperado";
      throw new Error(errMsg)
  }
};

// GET imágenes por fecha (ejemplo: /imagenes/{id}?fecha=YYYY-MM-DD)
export const getImagenesByFecha = async (id, fecha) => {
  try{
    const res = await api.get(`/imagenes/${id}/buscar_por_dia`, {
      params: { fecha } 
    });
    console.log(res.data)
    return res.data;
  } catch (err) {
      const errMsg = err.response?.data?.detail || "Ocurrió un error inesperado";
      throw new Error(errMsg)
  }
};

export const esAdminEnDispositivo = async (id) => {
  try {
    const dispositivoRes = await getDispositivoDetail(id);
    return await esAdminEnComedero(dispositivoRes.id_comedero);
  } catch (err) {
      const errMsg = err.response?.data?.detail || "Ocurrió un error inesperado";
      throw new Error(errMsg)
  }
};
