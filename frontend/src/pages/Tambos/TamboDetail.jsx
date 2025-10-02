// src/pages/Tambos/TamboDetail.jsx
import { useEffect, useState } from "react";
import { useNavigate, useParams, Link } from "react-router-dom";
import { esAdminEnTambo, getTamboDetail } from "../../services/tambo.service";
import AddUser from "./AddUser";
import AddComedero from "./AddComedero";
import { useAuthContext } from "../../context/AuthContext";

export default function TamboDetail() {
  const { id } = useParams();
  const { user } = useAuthContext();
  const [tambo, setTambo] = useState(null);
  const navigate = useNavigate();
  const [esAdmin, setEsAdmin] = useState(false);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchTambo();
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

  const handleGoBack = () => navigate(-1);

  if (isLoading){
    return <p>&#x21bb; Cargando información...</p>
  }

  if (!tambo) return (
    <div>
     <p>No se encontró información</p>
     {error && <p style={{ color: "red" }}>{error}</p>}
     <button onClick={handleGoBack}> &larr; Volver </button>
    </div>
  );

  return (
    <div>
      <h2>{tambo.nombre}</h2>
      <p>Descripción: {tambo?.descripcion || "No hay descripción"}</p>
      <p>Ubicación: {tambo.ubicacion}</p>

      {esAdmin &&  (
        <>
          <h3>Usuarios</h3>
          <ul>
            {tambo.usuarios.map((u) => (
              <li key={u.usuario.id}>
                {u.usuario.nombres} ({u.usuario.email}) &rarr; {u.rol?.nombre}
              </li>
            ))}
          </ul>
          <AddUser tamboId={id} onUserAdded={fetchTambo} />
        </>
      )}

      <h3>Comederos</h3>
      {tambo.comederos.length === 0 ? 
      (<p> No hay comederos asociados</p>
      ) : (
      <ul>
        <p>Haga clic sobre el comedero al que desee entrar</p>
        {tambo.comederos?.map((c) => (
          <li key={c.id}>{/*{c.nombre}*/}
            <Link to={`/comederos/${c.id}`}>{c.nombre}</Link>
          </li>
        ))}
      </ul>)}

      {esAdmin && (
      <AddComedero tamboId={id} onComederoAdded={fetchTambo}  />
      )}
      <br /><br />
      <button onClick={handleGoBack}> &larr; Volver </button>
    </div>
  );
}

