// src/services/tambo.service.js
import api from "../api/api";

export const getTambosByUser = async () => {
  try{
    const res = await api.get("/propios-tambos");
    return res.data;
  } catch (err) {
    const errMsg = err.response?.data?.detail || "Ocurrió un error inesperado";
    throw new Error(errMsg)
  }
};

export const createTambo = async (nombre, descripcion, ubicacion) => {
  try{
    const nuevoTambo = {
      nombre,
      descripcion,
      ubicacion
    }
    const res = await api.post("/tambos/", nuevoTambo);
    return res.data;
  } catch (err) {
    const errMsg = err.response?.data?.detail || "Ocurrió un error inesperado";
    throw new Error(errMsg)
  }
};

export const esAdminEnTambo = async (id) => {
  try{
    const asociaciones = await api.get("/propios-tambos");
    const asociacion = asociaciones.data.find(
      (a) => a.tambo.id === Number(id)
    );
    
    return asociacion.rol.es_admin;
  } catch (err) {
    const errMsg = err.response?.data?.detail || "Ocurrió un error inesperado";
    throw new Error(errMsg)
  }
}

export const getUserByEmail = async (email) => {
  try{
    const res = await api.get("/usuarios/buscar_por_mail", {
      params: {email}
    });
    const id = res.data.id
    return id;
  } catch (err) {
    const errMsg = err.response?.data?.detail || "Ocurrió un error inesperado";
    throw new Error(errMsg)
  }
}

export const getTamboDetail = async (id) => {
  let tamboRes = null
  try{
    tamboRes = await api.get(`/tambos/${id}`)
  } catch (err) {
    const errMsg = err.response?.data?.detail || "Ocurrió un error inesperado";
    throw new Error(errMsg)
  }

  let comederosRes = {data: []};
  try{
    comederosRes = await api.get(`/comederos/${id}/tambo`);
  } catch (err) {
    const errMsg = err.response?.data?.detail || "Ocurrió un error inesperado";
    throw new Error(errMsg)
  }

  let usuariosRes = { data: [] };

  // si es admin en este tambo, se traen los usuarios
  try{
    if (await esAdminEnTambo(id)){
      usuariosRes = await api.get(`/tambos/${id}/usuarios`);
    }
  } catch (err) {
    const errMsg = err.response?.data?.detail || "Ocurrió un error inesperado";
    throw new Error(errMsg)
  }

  return {
    ...tamboRes.data,
    usuarios: usuariosRes.data,
    comederos: comederosRes.data,}

};

export const getRoles = async () => {
  try{
    const res = await api.get(`/roles`);

    return res.data
  } catch (err) {
    const errMsg = err.response?.data?.detail || "Ocurrió un error inesperado";
    throw new Error(errMsg)
  }
}

export const addUserToTambo = async (usuarioId, tamboId, rolId) => {
  try{
    const res = await api.post(`/usuarios/${usuarioId}/tambos/${tamboId}/rol/${rolId}`);
    return res.data;
  } catch (err) {
    const errMsg = err.response?.data?.detail || "Ocurrió un error inesperado";
    throw new Error(errMsg)
  }
};

export const addComederoToTambo = async (tamboId, nombre, descripcion, ubicacion) => {
  try{
    const nuevoComedero = {
      nombre: nombre,
      descripcion: descripcion,
      ubicacion: ubicacion,
      id_tambo: tamboId
    };
    const res = await api.post("/comederos/",
      nuevoComedero,
    );

    return res.data;
  } catch (err) {
    const errMsg = err.response?.data?.detail || "Ocurrió un error inesperado";
    throw new Error(errMsg)
  }
};
