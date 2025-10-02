import { useEffect, useState } from "react";
import { useNavigate, useParams, Link } from "react-router-dom";
import { getComederoDetail, esAdminEnComedero } from "../../services/comedero.service";
import AddDevice from "./AddDevice";

export default function ComederoDetail() {
  const { id } = useParams();
  const [comedero, setComedero] = useState(null);
  const [esAdmin, setEsAdmin] = useState(false);
  const navigate = useNavigate();
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    fetchComedero();
  }, [id]);

  useEffect(() => {
    checkEsAdmin();
  }, [id]);

  const fetchComedero = async () => {
    try{
      const data = await getComederoDetail(id);
      setComedero(data);
      setIsLoading(false);
    } catch (err){
      setError(err.message);
      setIsLoading(false);
    }
  };
  
  const checkEsAdmin = async () => {
    try{
      const es_admin = await esAdminEnComedero(id);
      setEsAdmin(es_admin);
    } catch (err){
      setError(err.message);
    }
  }

  const handleGoBack = () => navigate(-1);

  if (isLoading){
    return <p>&#x21bb; Cargando información...</p>
  }
  
  if (!comedero) {
    return (
      <div>
        <p>No se encontró información del comedero</p>
        {error && <p style={{ color: "red" }}>{error}</p>}
        <button onClick={handleGoBack}> &larr; Volver </button>
      </div>
    );
  }

  return (
    <div>
      <h2>{comedero?.nombre || "No hay nombre"}</h2>
      <p>Descripción: {comedero?.descripcion || "No hay descripción"}</p>
      <p>Ubicación: {comedero.ubicacion}</p>

      <h3>Dispositivos</h3>
      {comedero?.dispositivos?.length === 0 ? (
        <>
        <p>No hay dispositivos asociados</p>
        {error && <p style={{ color: "red" }}>{error}</p>}
        </>
      ) : (
        <ul>
          <p>Haga clic sobre el dispositivo al que desee entrar</p>
          {comedero?.dispositivos?.map((d) => (
            <li key={d.id}>
              <Link to={`/dispositivos/${d.id}`}>{d.nombre}</Link>
            </li>
          ))}
        </ul>
      )}

      {esAdmin && <AddDevice comederoId={id} onDeviceAdded={fetchComedero} />}

      <br /><br />
      <button onClick={handleGoBack}> &larr; Volver </button>
    </div>
  );
}
