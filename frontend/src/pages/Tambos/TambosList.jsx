// src/pages/Tambos/TambosList.jsx
import { useEffect, useState } from "react";
import { getTambosByUser } from "../../services/tambo.service";
import { Link } from "react-router-dom";
import { useAuthContext } from "../../context/AuthContext";
import TamboAdd from "./TamboAdd";
import UsuarioPanel from "../Usuarios/UsuarioPanel";

export default function TambosList() {
  const { logout } = useAuthContext();
  const [asociaciones, setAsociaciones] = useState([]);
  const [setNombre] = useState("");
  const [setDescripcion] = useState("");
  const [setUbicacion] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    fetchAsociaciones();
  }, []);

  const fetchAsociaciones = async () => {
    try{
      const data = await getTambosByUser();
      setAsociaciones(data);
      setIsLoading(false)
    } catch (err){
      setError(err.message);
      setIsLoading(false)
    }
  };

  const handleCancel = () => {
    setShowForm(false);
    setNombre("");
    setDescripcion("");
    setUbicacion("");
  };

  if (isLoading){
    return <p>&#x21bb; Cargando información...</p>
  }

  return (
    <div className="grid-container">
      <div className="usuario-panel">
        <UsuarioPanel />
      </div>
      <div>
        <h1 className="title">Agro IoT</h1>
        <h2>Mis Tambos</h2>
        {error && <p className="text-error">{error}</p>}
        {asociaciones.length === 0 ? (
            <div>
              <p>En esta sección aparecerán los tambos a los que usted está asociado. Puede crear uno, o pedir al administrador de un tambo que lo asocie para comezar a utilizar el sistema.</p>
            </div>
          ) : (
            <div>
              <p>Haga clic sobre el tambo al que desee entrar.</p>
              <ul>
                {asociaciones.map((a) => (
                  <li key={a.tambo.id} className="items">
                    <Link to={`/tambos/${a.tambo.id}`} className="items">{a.tambo.nombre} ({a.rol.nombre})</Link>
                  </li>
                ))}
              </ul>
            </div>
          )}

        {!showForm ? (
          <button 
          onClick={() => setShowForm(true)}
          className="btn-create">
            + Crear tambo</button>
        ) : (
          <TamboAdd 
            onTamboCreated={fetchAsociaciones}
            onCancel={handleCancel}
          />
        )}
      </div>
    </div>
  );
}
