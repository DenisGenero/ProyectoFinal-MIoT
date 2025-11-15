/*import { useEffect, useState } from "react";
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
        <h1 style={{color:"#646cff"}}>Agro IoT</h1>
        <p>No se encontró información del comedero</p>
        {error && <p style={{ color: "red" }}>{error}</p>}
        <button onClick={handleGoBack}> &larr; Volver </button>
      </div>
    );
  }

  return (
    <div>
      <h1 style={{color:"#646cff"}}>Agro IoT</h1>
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
*/
import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { getComederoDetail, esAdminEnComedero } from "../../services/comedero.service";
import AddDevice from "./AddDevice";
import DispositivoDetail from "../Dispositivos/DispositivoDetail";

export default function ComederoDetail() {
  const { id } = useParams();
  const [comedero, setComedero] = useState(null);
  const [esAdmin, setEsAdmin] = useState(false);
  const [selectedDeviceId, setSelectedDeviceId] = useState(null);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    fetchComedero();
    checkEsAdmin();
  }, [id]);

  const fetchComedero = async () => {
    try {
      const data = await getComederoDetail(id);
      setComedero(data);
      setIsLoading(false);
    } catch (err) {
      setError(err.message);
      setIsLoading(false);
    }
  };

  const checkEsAdmin = async () => {
    try {
      const es_admin = await esAdminEnComedero(id);
      setEsAdmin(es_admin);
    } catch (err) {
      setError(err.message);
    }
  };

  const handleGoBack = () => navigate(-1);

  if (isLoading) return <p>&#x21bb; Cargando información...</p>;

  if (!comedero)
    return (
      <div>
        <p>No se encontró información del comedero</p>
        {error && <p style={{ color: "red" }}>{error}</p>}
        <button onClick={handleGoBack}> &larr; Volver </button>
      </div>
    );

  return (
    <div>
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr", //selectedDeviceId ? "1fr 1fr" : "1fr",
          gap: "2rem",
          alignItems: "start",
        }}
      >
        {/* Columna 1: Comedero */}
        <div>
          <h1 style={{ color: "#646cff" }}>Agro IoT</h1>
          <h2>{comedero?.nombre || "Sin nombre"}</h2>
          <p><b>Descripción:</b> {comedero?.descripcion || "No hay descripción"}</p>
          <p><b>Ubicación:</b> {comedero.ubicacion}</p>
        
          <div
            style={{
              border: "1px solid #ccc",
              borderRadius: "10px",
              padding: "1rem",
              paddingTop: "1%",
              boxShadow: "0 2px 6px rgba(0,0,0,0.1)",
            }}
          >
            <h3>Dispositivos</h3>
            {comedero?.dispositivos?.length === 0 ? (
              <>
                <p>No hay dispositivos asociados</p>
                {error && <p style={{ color: "red" }}>{error}</p>}
              </>
            ) : (
              <ul>
                <p>Haga clic sobre el dispositivo que desee ver</p>
                {comedero?.dispositivos?.map((d) => (
                  <li
                    key={d.id}
                    style={{
                      cursor: "pointer",
                      color: "#646cff",
                      //textDecoration: "underline",
                      marginBottom: "0.5rem",
                    }}
                    onClick={() => setSelectedDeviceId(d.id)}
                  >
                    {d.nombre}
                  </li>
                ))}
              </ul>
            )}

            {esAdmin && <AddDevice comederoId={id} onDeviceAdded={fetchComedero} />}
            
          </div>
          <br />
          <button onClick={handleGoBack}> &larr; Volver </button>
        </div>

        {/* Columna 2: Dispositivo seleccionado */}
        {selectedDeviceId && (
          <div
            style={{
              border: "1px solid #ccc",
              borderRadius: "10px",
              padding: "1rem",
              paddingTop: "5%",
              marginTop: "25%",
              boxShadow: "0 2px 6px rgba(0,0,0,0.1)",
            }}
          >
            <button
              onClick={() => setSelectedDeviceId(null)}
              style={{
                background: "#646cff",
                border: "none",
                padding: "0.4rem 0.8rem",
                borderRadius: "5px",
                cursor: "pointer",
                marginBottom: "0.8rem",
              }}
            >
              ✖ Ocultar dispositivo
            </button>

            {/* Renderizamos DispositivoDetail dentro de un iframe-like */}
            <DispositivoDetail id={selectedDeviceId}/>
          </div>
        )}
      </div>
    </div>
  );
}
