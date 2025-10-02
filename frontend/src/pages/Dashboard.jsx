// src/pages/Dashboard.jsx
import { useAuthContext } from "../context/AuthContext";

export default function Dashboard() {
  const { user, logout } = useAuthContext();

  return (
    <div>
      <h2>Bienvenido {user?.email}</h2>
      <button onClick={logout}>Cerrar sesión</button>
    </div>
  );
}
