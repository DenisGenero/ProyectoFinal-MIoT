// src/pages/Tambos/AddUser.jsx
import { useEffect, useState } from "react";
import { addUserToTambo, getRoles, getUserByEmail } from "../../services/tambo.service";

export default function AddUser({ tamboId, onUserAdded }) {
  const [email, setEmail] = useState("");
  const [roles, setRoles] = useState([]); // lista de roles de la DB
  const [selectedRolId, setSelectedRolId] = useState(""); // rol elegido
  const [showForm, setShowForm] = useState(false);

  useEffect(() => {
    fetchRoles();
  }, []);

  const fetchRoles = async () => {
    try {
      const data = await getRoles();
      setRoles(data);
      if (data.length > 0) setSelectedRolId(data[0].id); // default primer rol
    } catch (err) {
      console.error("Error al cargar roles:", err);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const userId = await getUserByEmail(email)
    console.log("Id1:", userId);
    await addUserToTambo(userId, tamboId, selectedRolId);
    setEmail("");
    onUserAdded();
    setShowForm(false);
  };

  const handleCancel = () => {
    setShowForm(false);
    setEmail("");
    setSelectedRolId(roles[0]?.id || "");
  };

  return (
    <>
      {!showForm ? (
        <button onClick={() => setShowForm(true)}>Asociar usuario</button>
      ) : (
        <form onSubmit={handleSubmit}>
          <h4>Asociar usuario</h4>
          <input
            type="email"
            placeholder="Email del usuario"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <select
            value={selectedRolId}
            onChange={(e) => setSelectedRolId(e.target.value)}
          >
            {roles.map((rol) => (
              <option key={rol.id} value={rol.id}>
                {rol.nombre}
              </option>
            ))}
          </select>
          <br />
          <button type="submit">Agregar</button>
          <button type="button" onClick={handleCancel}>
            Cancelar
          </button>
        </form>
      )}
    </>
  );
}
