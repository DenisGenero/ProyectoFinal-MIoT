import { useState } from "react";
import { addComederoToTambo } from "../../services/tambo.service";

export default function AddComedero({ tamboId, onComederoAdded }) {
  const [nombre, setNombre] = useState("");
  const [descripcion, setDescripcion] = useState("");
  const [ubicacion, setUbicacion] = useState("");
  const [showForm, setShowForm] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await addComederoToTambo(tamboId, nombre, descripcion, ubicacion);
      setNombre("");
      setDescripcion("");
      setUbicacion("");
      setShowForm(false);
      onComederoAdded();
    } catch (err) {
      console.error("Error al agregar comedero:", err);
    }
  };

  if (!showForm) {
    return <button onClick={() => setShowForm(true)}
    style={{backgroundColor:"green"}}>
      + Agregar comedero</button>;
  }

  return (
    <form onSubmit={handleSubmit}>
      <h4>Agregar comedero</h4>
      <input
        type="text"
        placeholder="Nombre"
        value={nombre}
        onChange={(e) => setNombre(e.target.value)}
        required
        style={{ width: '60%' }}
      /> 
      <br /><br />
      <input
        type="text"
        placeholder="Descripción"
        value={descripcion}
        onChange={(e) => setDescripcion(e.target.value)}
        style={{ width: '60%' }}
      />
      <br /><br />
      <input
        type="text"
        placeholder="Ubicación"
        value={ubicacion}
        onChange={(e) => setUbicacion(e.target.value)}
        required
        style={{ width: '60%' }}
      />
      <br /><br />
      <button type="submit"
      style={{ backgroundColor:"green" }}>
        + Agregar</button> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
      <button type="button" onClick={() => setShowForm(false)}
      style={{ backgroundColor:"red" }}  >
        X Cancelar
      </button>
    </form>
  );
}
