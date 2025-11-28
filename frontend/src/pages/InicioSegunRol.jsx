import { useEffect, useState } from "react";
import { Navigate } from "react-router-dom";
import { getUserInfo } from "../services/auth.service";

export default function InicioSegunRol() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    cargarUsuario();
  }, []);

  async function cargarUsuario() {
    try {
      const data = await getUserInfo();
      setUser(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  }

  // Mientras no se cargó el usuario → no retornes nada
  if (loading) return null;

  // Cuando ya se cargó:
  if (user?.es_superadmin) {
    return <Navigate to="/superadmin" />;
  }

  return <Navigate to="/tamboslist" />;
}
