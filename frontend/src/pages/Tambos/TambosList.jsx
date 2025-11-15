// src/pages/Tambos/TambosList.jsx
import { useEffect, useState } from "react";
import { getTambosByUser, createTambo, esAdminEnTambo } from "../../services/tambo.service";
import { Link, useParams } from "react-router-dom";
import { useAuthContext } from "../../context/AuthContext";

export default function TambosList() {
  const { logout } = useAuthContext();
  const [asociaciones, setAsociaciones] = useState([]);
  const [nombre, setNombre] = useState("");
  const [descripcion, setDescripcion] = useState("");
  const [ubicacion, setUbicacion] = useState("");
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

  const handleCreate = async (e) => {
    e.preventDefault();
    try{
      await createTambo(nombre, descripcion, ubicacion);
      setNombre("");
      setDescripcion("");
      setUbicacion("");
      setShowForm(false);
      fetchAsociaciones();
    } catch (err) {
      setError(err.message);
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
    <div>
      <h1 style={{color:"#646cff"}}>Agro IoT</h1>
      <h2>Mis Tambos</h2>
      {error && <p style={{ color: "red" }}>{error}</p>}
      {asociaciones.length === 0 ? (
          <>
            <p>En esta sección aparecerán los tambos a los que usted está asociado. Puede crear uno, o pedir al administrador de un tambo que lo asocie para comezar a utilizar el sistema.</p>
          </>
        ) : (
          <>
            <p>Haga clic sobre el tambo al que desee entrar.</p>
            <ul>
              {asociaciones.map((a) => (
                <li key={a.tambo.id}>
                  <Link to={`/tambos/${a.tambo.id}`}>{a.tambo.nombre}</Link>
                  {" "}
                  <span style={{ fontStyle: "italic" }}>
                    ({a.rol.nombre})
                  </span>
                </li>
              ))}
            </ul>
          </>
        )}

      {!showForm ? (
        <button 
        onClick={() => setShowForm(true)}
        style={{backgroundColor:"green",}}>
          + Crear tambo</button>
      ) : (
        <form onSubmit={handleCreate}
        >
          <h3>Crear un nuevo tambo</h3>
          <input
            type="text"
            placeholder="Nombre"
            value={nombre}
            onChange={(e) => setNombre(e.target.value)}
            required
          />
          <br /><br />
          <input
            type="text"
            placeholder="Descripción"
            value={descripcion}
            onChange={(e) => setDescripcion(e.target.value)}
          />
          <br /><br />
          <input
            type="text"
            placeholder="Ubicación"
            value={ubicacion}
            onChange={(e) => setUbicacion(e.target.value)}
            required
          />
          <br /><br />
          <button className="boton-crear" type="submit">Crear</button>
          <button type="button" onClick={handleCancel}>
            Cancelar
          </button>
        </form>
      )}
      <br /><br />
      <button onClick={logout}
      style={{backgroundColor:"red",}}>
        Cerrar sesión</button>
    </div>
  );
}
