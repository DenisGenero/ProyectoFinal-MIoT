// src/pages/Tambos/TamboDetail.jsx
import { useEffect, useState } from "react";
import { useNavigate, useParams, Link } from "react-router-dom";
import { esAdminEnTambo, getTamboDetail, getRoles } from "../../services/tambo.service";
import ComederoAdd from "../Comederos/ComederoAdd";
import UsuarioList from "../Usuarios/UsuariosList";
import UsuarioAdd from "../Usuarios/UsuarioAdd";
import ComederoList from "../Comederos/ComederoList";
import TamboEdit from "./TamboEdit";
import UsuarioPanel from "../Usuarios/UsuarioPanel";


export default function TamboDetail() {
  const { id } = useParams();
  const [tambo, setTambo] = useState(null);
  const [roles, setRoles] = useState(null);
  const [selectedRolId, setSelectedRolId] = useState("");
  const [esAdmin, setEsAdmin] = useState(false);
  const [error, setError] = useState("");
  const [showEditForm, setShowEditForm] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    fetchTambo();
    fetchRoles();
    checkEsAdmin();
  }, [id]);

  const fetchTambo = async () => {
    try {
      const data = await getTamboDetail(id);
      setTambo(data);
      setIsLoading(false)
    } catch (err) {
      setError(err.message);
      setIsLoading(false)
    }
  };

  const fetchRoles = async () => {
    try {
      const data = await getRoles();
      setRoles(data);
      if (data.length > 0) setSelectedRolId(data[0].id); // default primer rol
    } catch (err) {
      console.error("Error al cargar roles:", err);
    }
  };

  const checkEsAdmin = async () => {
    try {
      const es_admin = await esAdminEnTambo(id);
      setEsAdmin(es_admin);
    } catch (err) {
      setError(err.message);
    }
  }

  const handleGoBack = () => navigate(-1);

  if (isLoading) return <p>&#x21bb; Cargando información...</p>

  if (!tambo) return (
    <div>
      <p>No se encontró información</p>
      {error && <p className="text-error">{error}</p>}
      <button onClick={handleGoBack} className="btn-back"> &larr; Volver </button>
    </div>
  );

  return (
      <div className="grid-container" >
        {/*Fila 1 - Columna 1 */}
        <div className="usuario-panel">
          <UsuarioPanel />
          <button onClick={handleGoBack} className="btn-back">&larr; Volver</button>
        </div>
        {/*Fila 1 - Columna 2 */}
        <div>
          <h1 className="title">Agro IoT</h1>
          {esAdmin ? (
            showEditForm ? (
              <TamboEdit
                tambo={tambo}
                onCancel={() => setShowEditForm(false)}
                onSaved={() => {
                  setShowEditForm(false);
                  fetchTambo();
                }}
              />
            ) : (
            <div>
              <h2>{tambo.nombre}</h2>
              <p><b>Descripción:</b> {tambo?.descripcion || "No hay descripción"}</p>
              <p><b>Ubicación:</b> {tambo.ubicacion}</p>
              <button onClick={() => setShowEditForm(true)} className="btn-edit">
                Editar tambo
              </button>
            </div>
            ) 
          ) : (
            <>
              <h2>{tambo.nombre}</h2>
              <p><b>Descripción:</b> {tambo?.descripcion || "No hay descripción"}</p>
              <p><b>Ubicación:</b> {tambo.ubicacion}</p>
            </>
          )}
        </div>
        {/*Fila 1 - Columna 3 */}
        <div></div>
        {/*Fila 2 - Columna 1 */}
        {esAdmin && (
          <div className="card">
            <UsuarioList 
              tambo={tambo}
              roles={roles}
              onTamboUpdate={fetchTambo}/>
              <br />
              <UsuarioAdd
              tamboId={id}
              onUserAdded={fetchTambo}
              roles={roles}
              selectedRolId={selectedRolId}
            />
          </div>
        )}

        <div className="card">
          <ComederoList comederos={tambo.comederos}/>
          {esAdmin && <ComederoAdd tamboId={id} onComederoAdded={fetchTambo} />}
        </div>
      </div>
  );
}

