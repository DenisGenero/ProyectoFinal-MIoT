import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { getComederoDetail, esAdminEnComedero } from "../../services/comedero.service";
import AddDevice from "../Dispositivos/DispositivoAdd";
import DispositivoDetail from "../Dispositivos/DispositivoDetail";
import ComederoEdit from "./ComederoEdit";
import UsuarioPanel from "../Usuarios/UsuarioPanel";

export default function ComederoDetail() {
  const { id } = useParams();
  const [comedero, setComedero] = useState(null);
  const [esAdmin, setEsAdmin] = useState(false);
  const [selectedDeviceId, setSelectedDeviceId] = useState(null);
  const [showEditForm, setShowEditForm] = useState(false);
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
      <div className="grid-container">
        <div className="usuario-panel">
          <UsuarioPanel />
          <br />
          <br />
          <button onClick={handleGoBack}> &larr; Volver </button>
        </div>
        <div>
          <h1 className="title">Agro IoT</h1>
          {esAdmin ? (
            showEditForm ? (
              <ComederoEdit
                comedero={comedero}
                onCancel={() => setShowEditForm(false)}
                onSaved={() => {
                  setShowEditForm(false);
                  fetchComedero();
                }}
              />
            ) : (
              <>
                <h2>{comedero.nombre}</h2>
                <p><b>Descripción:</b> {comedero.descripcion || "No hay descripción"}</p>
                <p><b>Ubicación:</b> {comedero.ubicacion || "No hay ubicación"}</p>
                <button onClick={() => setShowEditForm(true)} className="btn-edit">Editar comedero</button>
                <br /><br />
              </>
            )
          ) : (
            <>
              <h2>{comedero.nombre}</h2>
              <p><b>Descripción:</b> {comedero.descripcion || "No hay descripción"}</p>
              <p><b>Ubicación:</b> {comedero.ubicacion || "No hay ubicación"}</p>
            </>
          )}

        
          <div className="card" >
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
                    onClick={() => {selectedDeviceId ? (setSelectedDeviceId(null)) : (setSelectedDeviceId(d.id))}}
                    className="items"
                  >
                    {d.nombre}
                  </li>
                ))}
              </ul>
            )}

            {esAdmin && <AddDevice comederoId={id} onDeviceAdded={fetchComedero} />}
            
          </div>
        </div>

        {/* Columna 2: Dispositivo seleccionado */}
        {selectedDeviceId && (
          <div className="card" style={{marginTop:"33%"}}>
            <DispositivoDetail id={selectedDeviceId}/>
            <br />
            <button
              onClick={() => setSelectedDeviceId(null)}
              className="btn-close"
            >
              Ocultar
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
