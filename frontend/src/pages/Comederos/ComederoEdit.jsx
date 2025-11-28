// src/pages/Comederos/ComederoEdit.jsx

import { useState } from "react";
import { EditComedero } from "../../services/comedero.service";

export default function ComederoEdit({ comedero, onCancel, onSaved }) {
  const [nombre, setNombre] = useState(comedero.nombre);
  const [descripcion, setDescripcion] = useState(comedero.descripcion || "");
  const [ubicacion, setUbicacion] = useState(comedero.ubicacion || "");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await EditComedero(comedero.id, {
        nombre,
        descripcion,
        ubicacion
      });
      onSaved(); // avisa al padre que recargue los datos
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <>
      <h3>Editar Comedero</h3>
      {error && <p className="text-error">{error}</p>}

      <form onSubmit={handleSubmit}>
        <div>
          <label style={{ display: "inline-block", width: "30%" }}>
            <b>Nombre:</b>
          </label>
          <input
            value={nombre}
            onChange={(e) => setNombre(e.target.value)}
          />
        </div>

        <br />

        <div>
          <label style={{ display: "inline-block", width: "30%" }}>
            <b>Descripción:</b>
          </label>
          <input
            value={descripcion}
            onChange={(e) => setDescripcion(e.target.value)}
          />
        </div>

        <br />

        <div>
          <label style={{ display: "inline-block", width: "30%" }}>
            <b>Ubicación:</b>
          </label>
          <input
            value={ubicacion}
            onChange={(e) => setUbicacion(e.target.value)}
          />
        </div>

        <br />

        <button className="btn-save" type="submit">
          Guardar
        </button>

        <button
          type="button"
          onClick={onCancel}
          className="btn-cancel"
        >
          Cancelar
        </button>
      </form>

      <br />
    </>
  );
}
