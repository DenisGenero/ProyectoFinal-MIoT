// src/pages/Tambos/TamboDetail.jsx
import { useEffect, useState } from "react";
import { useNavigate, useParams, Link } from "react-router-dom";
import { esAdminEnTambo, getTamboDetail, desvincularUsuarioDeTambo, actualizarRolEnTambo, getRoles } from "../../services/tambo.service";
import AddUser from "./AddUser";
import AddComedero from "./AddComedero";
import { useAuthContext } from "../../context/AuthContext";


export default function TamboDetail() {
  const { id } = useParams();
  const { user } = useAuthContext();
  const [tambo, setTambo] = useState(null);
  const [roles, setRoles] = useState(null);
  const [selectedRolId, setSelectedRolId] = useState(""); // rol elegido
  const navigate = useNavigate();
  const [esAdmin, setEsAdmin] = useState(false);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const [selectedUser, setSelectedUser] = useState(null);
  const [showForm, setShowForm] = useState(false);

  useEffect(() => {
    fetchTambo();
    fetchRoles();
  }, [id]);

  useEffect(() => {
    checkEsAdmin();
  }, [id]);

  const fetchTambo = async () => {
    try{
      const data = await getTamboDetail(id);
      setTambo(data);
      setIsLoading(false)
    } catch (err) {
      setError(err.message);
      setIsLoading(false)
    }
  };

  const checkEsAdmin = async () => {
    try{
      const es_admin = await esAdminEnTambo(id);
      setEsAdmin(es_admin);
    } catch (err){
      setError(err.message);
    }
  }

    const fetchRoles = async () => {
      try {
        const data = await getRoles();
        setRoles(data);
        if (data.length > 0) setSelectedRolId(data[0].id); // default primer rol
      } catch (err) {
        console.error("Error al cargar roles:", err);
      }
    };

  const handleBajaUsuario = async (userId, tamboId) => {
    console.log(`TamboID: ${tamboId}`)
    if (window.confirm("¿Seguro que desea desvincular este usuario del tambo?")) {
      try {
        await desvincularUsuarioDeTambo(userId, tamboId);
        fetchTambo();
        setSelectedUser(null);
      } catch (err) {
        alert("Error al dar de baja al usuario: "+ err);
      }}
  };

const handleChangeRol = async (userId, tamboId, nuevoRolId) => {
  try {
    await actualizarRolEnTambo(userId, tamboId, nuevoRolId); // tu endpoint
    fetchTambo();
  } catch (err) {
    alert("Error al actualizar el rol:" + err);
  }
};

  const handleGoBack = () => navigate(-1);

  if (isLoading) return <p>&#x21bb; Cargando información...</p>

  if (!tambo) return (
    <div>
      <p>No se encontró información</p>
      {error && <p className="text-error">{error}</p>}
      <button onClick={handleGoBack}> &larr; Volver </button>
    </div>
  );

  return (
    <div>
      <h1 className="title">Agro IoT</h1>
      <h2>{tambo.nombre}</h2>
      <p><b>Descripción:</b> {tambo?.descripcion || "No hay descripción"}</p>
      <p><b>Ubicación:</b> {tambo.ubicacion}</p>

      <div
        style={{
          display: esAdmin ? "grid" : "block",
          gridTemplateColumns: esAdmin ? "1fr 1fr" : "none",
          gap: esAdmin ? "4rem" : "0",
          alignItems: "start",
        }}
      >
        {esAdmin && (
          <div className="card">
            <h3>Usuarios</h3>
            <p>Haga clic sobre un usuario si desea desvincularlo o modificar su rol</p>
            <ul> {tambo.usuarios.map((u) => (
              <li
                key={u.usuario.id}
                onClick={() => setSelectedUser(selectedUser?.usuario.id === u.usuario.id ? null : u)}
                style={{
                  cursor: "pointer",
                  color: "#646cff",
                  padding: "1%",
                }}
              >
                <b>{u.usuario.nombres} {u.usuario.apellidos} → {u.rol?.nombre}</b>
                {selectedUser?.usuario.id === u.usuario.id && (
                  <div> 
                    <p style={{marginBottom:"0.1%", marginTop:"0.5%"}}><b>Mail: </b> {u.usuario.email}</p>
                    <label>
                      <b>Rol:</b>&nbsp;&nbsp;
                      <select
                        value={u.rol?.id || ""}
                        onChange={(e) => handleChangeRol(u.usuario.id, tambo.id, Number(e.target.value))}
                        onClick={(e) => e.stopPropagation()}
                      >
                        {roles.map((r) => (
                          <option key={r.id} value={r.id}>{r.nombre}</option>
                        ))}
                      </select>
                    </label> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    <button
                      style={{ marginTop: "0.4rem", background: "red", border: "none", borderRadius: "4px", padding: "0.3rem 0.6rem" }}
                      onClick={() => handleBajaUsuario(u.usuario.id, tambo.id)}
                    >
                      &#10006; Dar de baja
                    </button> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    <button
                      style={{ marginTop: "0.4rem", background: "#646cff", border: "none", borderRadius: "4px", padding: "0.3rem 0.6rem" }}
                      onClick={() => setSelectedUser(null)}
                    >
                      Ocultar
                    </button>
                  </div>
                )}
              </li>))}
            </ul>
            <AddUser tamboId={id} onUserAdded={fetchTambo} />
          </div>
        )}

        <div className="card">
          <h3>Comederos</h3>
          {tambo.comederos.length === 0 ? (
            <p>No hay comederos asociados</p>
          ) : (
            <ul>
              <p>Haga clic sobre el comedero al que desee entrar</p>
              {tambo.comederos?.map((c) => (
                <li key={c.id}
                style={{padding:"1%",}}
                >
                  <Link to={`/comederos/${c.id}`}>{c.nombre}</Link>
                </li>
              ))}
            </ul>
          )}
          {esAdmin && <AddComedero tamboId={id} onComederoAdded={fetchTambo} />}
        </div>
      </div>

      <br />
      <button onClick={handleGoBack}>&larr; Volver</button>
    </div>
  );
}

