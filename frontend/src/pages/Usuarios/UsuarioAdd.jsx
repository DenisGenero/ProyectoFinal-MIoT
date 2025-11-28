// src/pages/Tambos/AddUser.jsx
import { useEffect, useState } from "react";
import { addUserToTambo, getUserByEmail } from "../../services/tambo.service";

export default function UsuarioAdd({ tamboId, onUserAdded, roles, selectedRolId: defaultRolId }) {
  const [email, setEmail] = useState("");
  const [selectedRolId, setSelectedRolId] = useState(defaultRolId);
  const [showForm, setShowForm] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    setSelectedRolId(defaultRolId);
  }, [defaultRolId]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const userId = await getUserByEmail(email);
      await addUserToTambo(userId, tamboId, selectedRolId);

      setEmail("");
      setShowForm(false);
      onUserAdded();
    } catch (err) {
      setError(err.message);
    }
  };

  const handleCancel = () => {
    setShowForm(false);
    setEmail("");
    setSelectedRolId(defaultRolId); // vuelve al default
    setError("");
  };

  return (
    <>
      {!showForm ? (
        <button
          onClick={() => {
            setError("");
            setShowForm(true);
          }}
          className="btn-add"
        >
          Agregar usuario
        </button>
      ) : (
        <form onSubmit={handleSubmit}>
          <h4>Agregar usuario</h4>

          {error && <p style={{ color: "red" }}>{error}</p>}

          <input
            type="email"
            placeholder="Email del usuario"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            style={{ width: "60%" }}
          />
          &nbsp; &nbsp;

          <select
            value={selectedRolId}
            onChange={(e) => setSelectedRolId(e.target.value)}
            style={{ width: "30%" }}
          >
            {roles.map((rol) => (
              <option key={rol.id} value={rol.id}>
                {rol.nombre}
              </option>
            ))}
          </select>

          <br />

          <button type="submit" className="btn-add">
            Agregar
          </button>
          &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;

          <button
            type="button"
            onClick={handleCancel}
            className="btn-cancel"
          >
            Cancelar
          </button>
        </form>
      )}
    </>
  );
}
