import { useState } from "react";
import { addDeviceToComedero } from "../../services/comedero.service";

export default function AddDevice({ comederoId, onDeviceAdded }) {
  const [nombre, setNombre] = useState("");
  const [showForm, setShowForm] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await addDeviceToComedero(comederoId, nombre);
      setNombre("");
      setShowForm(false);
      onDeviceAdded();
    } catch (err) {
      console.error("Error al agregar dispositivo:", err);
    }
  };

  if (!showForm) {
    return <button onClick={() => setShowForm(true)}>Agregar dispositivo</button>;
  }

  return (
    <form onSubmit={handleSubmit}>
      <h4>Agregar nuevo dispositivo</h4>
      <input
        type="text"
        placeholder="Nombre"
        value={nombre}
        onChange={(e) => setNombre(e.target.value)}
        required
      /> 
      <br /><br />
      <button type="submit">Guardar</button>
      <button type="button" onClick={() => setShowForm(false)}>
        Cancelar
      </button>
    </form>
  );
}
