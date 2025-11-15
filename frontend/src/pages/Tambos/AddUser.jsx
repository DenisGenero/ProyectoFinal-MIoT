// src/pages/Tambos/AddUser.jsx
import { useEffect, useState } from "react";
import { addUserToTambo, getRoles, getUserByEmail } from "../../services/tambo.service";

export default function AddUser({ tamboId, onUserAdded }) {
  const [email, setEmail] = useState("");
  const [roles, setRoles] = useState([]); // lista de roles de la DB
  const [selectedRolId, setSelectedRolId] = useState(""); // rol elegido
  const [showForm, setShowForm] = useState(false);
  const [error, setError] = useState("");

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
    try{
      const userId = await getUserByEmail(email)
      await addUserToTambo(userId, tamboId, selectedRolId);
      setEmail("");
      onUserAdded();
      setShowForm(false);
    } catch(err){
      setError(err.message);
    }
  };

  const handleCancel = () => {
    setShowForm(false);
    setEmail("");
    setSelectedRolId(roles[0]?.id || "");
    setError("");
  };

  return (
    <>
      {!showForm ? (
        <button onClick={() => setShowForm(true)}
        style={{backgroundColor:"green"}}>
          + Asociar usuario</button>
      ) : (
        <form onSubmit={handleSubmit}>
          <h4>Asociar usuario</h4>
          {error && <p style={{ color: "red" }}>{error}</p>}
          <input
            type="email"
            placeholder="Email del usuario"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            style={{ width: '60%' }}
          /> &nbsp; &nbsp;
          <select
            value={selectedRolId}
            onChange={(e) => setSelectedRolId(e.target.value)}
            style={{ width: '30%' }}
          >
            {roles.map((rol) => (
              <option key={rol.id} value={rol.id}>
                {rol.nombre}
              </option>
            ))}
          </select>
          <br/>
          <br/>
          <button type="submit"
          style={{backgroundColor:"green"}}>
            + Agregar</button> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
          <button type="button" onClick={handleCancel}
          style={{backgroundColor:"red"}}>
            X Cancelar
          </button>
        </form>
      )}
    </>
  );
}
