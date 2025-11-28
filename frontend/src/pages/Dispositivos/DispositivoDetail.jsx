import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import {
  getDispositivoDetail,
  updateDispositivoConfig,
  getImagenesByFecha,
  esAdminEnDispositivo,
} from "../../services/dispositivo.service";
import DispositivoEdit from "./DispositivoEdit";
import InfoDispositivo from "./InfoDispositivo"
import BuscarImagenes from "./SearchImagenes"

export default function DispositivoDetail(props) {
  //const { id } = useParams(); // id del dispositivo
  const params = useParams();
  const id = props.id || params.id;
  const [dispositivo, setDispositivo] = useState(null);
  const [esAdmin, setEsAdmin] = useState(false);
  const [fecha, setFecha] = useState(""); // yyyy-mm-dd
  const [imagenes, setImagenes] = useState([]);
  const [editForm, setEditForm] = useState({
    nombre: "",
    hora_inicio: "",
    hora_fin: "",
    intervalo: 0,
  });
  const [mostrarForm, setMostrarForm] = useState(false);
  const navigate = useNavigate();
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchDispositivo();
  }, [id]);

  useEffect(() => {
    checkEsAdmin();
  }, [id]);

  const fetchDispositivo = async () => {
    try{
      const data = await getDispositivoDetail(id);
      setDispositivo(data);
      setEditForm({
        nombre: data?.nombre || "",
        hora_inicio: data?.hora_inicio || "No configurada",
        hora_fin: data?.hora_fin || "No configurada",
        intervalo: data?.intervalo || 30,
      });
      setIsLoading(false);
    } catch (err){
      setError(err.message);
      setIsLoading(false);
    }
  };

  const checkEsAdmin = async () => {
    try{
      const es_admin = await esAdminEnDispositivo(id);
      setEsAdmin(es_admin);
    } catch (err){
      setError(err.message);
    }
  }

  const handleGoBack = () => navigate(-1);

  const handleFechaChange = (e) => {
    setFecha(e.target.value);
  };
  
  const handleSearchClick = async () => {
    if (fecha) {
      try {
        const data = await getImagenesByFecha(id, fecha);
        setImagenes(data);
      } catch (error) {
        console.error("Error al buscar imágenes:", error);
        setImagenes([]);
      }
    }
  };

  const handleFormChange = (e) => {
    setEditForm({ ...editForm, [e.target.name]: e.target.value });
  };

  const handleUpdate = async (e) => {
    e.preventDefault();
    try {
      await updateDispositivoConfig(id, editForm);
      await fetchDispositivo();
      setMostrarForm(false);
      alert("Dispositivo actualizado");
    } catch (err) {
      console.error("Error al actualizar dispositivo:", err);
      alert("Error al actualizar");
    }
  };

  const handleCancelEdit = () => {
    setMostrarForm(false);
    setEditForm({
      nombre: dispositivo?.nombre || "",
      hora_inicio: dispositivo?.hora_inicio || "",
      hora_fin: dispositivo?.hora_fin || "",
      intervalo: dispositivo?.intervalo || 0,
    });
  };

  if (isLoading){
    return <p>&#x21bb; Cargando información...</p>
  }

  if (!dispositivo) {
    return (
      <div>
        <p>No se encontró información del dispositivo</p>
        <button onClick={handleGoBack}> &larr; Volver </button>
      </div>
    );
  }

  return (
    <div>
      {!esAdmin ? (
        <>
          <InfoDispositivo dispositivo={dispositivo}/>
          <BuscarImagenes
              fecha={fecha}
              handleFechaChange={handleFechaChange}
              handleSearchClick={handleSearchClick}
              imagenes={imagenes}
            />
        </>
      ) : (
        <>
          {!mostrarForm ? (
            <>
                <InfoDispositivo dispositivo={dispositivo}/>
                <button onClick={() => setMostrarForm(true)}>Actualizar</button>
                <BuscarImagenes
                  fecha={fecha}
                  handleFechaChange={handleFechaChange}
                  handleSearchClick={handleSearchClick}
                  imagenes={imagenes}
                />
            </>
          ) : (
            <DispositivoEdit
              editForm={editForm}
              handleFormChange={handleFormChange}
              handleUpdate={handleUpdate}
              onCancel={handleCancelEdit}
            />
          )}
        </>
      )}
    </div>
  );
}
