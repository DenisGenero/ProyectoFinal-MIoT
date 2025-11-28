import UsuarioPanel from "./UsuarioPanel";
import { useState } from "react";
import {
  getAllDevices,
  getUnconfiguredDevices,
  getDevicesByTambo,
  getDevicesByComedero,
  getDevicesByUser,
  findUserByEmail,
  promoteToSuperuser,
} from "../../services/superadmin.service";
import DispositivoList from "../Dispositivos/DispositivoList";

export default function PanelSuperadmin() {
  const [devices, setDevices] = useState([]);
  const [userResult, setUserResult] = useState(null);
  const [email, setEmail] = useState("");

  const buscarTodos = async () => {
    const data = await getAllDevices();
    setDevices(data);
  };

  const buscarNoConfig = async () => {
    const data = await getUnconfiguredDevices();
    setDevices(data);
  };

  const buscarPorTambo = async (id) => {
    const data = await getDevicesByTambo(id);
    setDevices(data);
  };

  const buscarPorComedero = async (id) => {
    const data = await getDevicesByComedero(id);
    setDevices(data);
  };

  const buscarPorUsuario = async (id) => {
    const data = await getDevicesByUser(id);
    setDevices(data);
  };

  const buscarUsuario = async () => {
    if (!email) return;
    const data = await findUserByEmail(email);
    setUserResult(data);
  };

  const hacerSuper = async (userId) => {
    await promoteToSuperuser(userId);
    alert("Usuario promovido a superadministrador.");
  };

  return (
    <div className="grid-container">
        <div className="usuario-panel">
            <UsuarioPanel />
        </div>
        <div>
          <h1 className="title">Agro IoT </h1>
          <h2> Panel de Superadministrador</h2>
        </div>
        <div style={{gridRow:"2", gridColumn:"2"}} className="card">
          <DispositivoList />
        </div>

        <div style={{gridRow:"2", gridColumn:"3"}}>
          <h2>Buscar usuario por email</h2>
          <input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="email" />
          <button onClick={buscarUsuario}>Buscar</button>

          {userResult && (
            <div>
              <p>Usuario encontrado: {userResult.email}</p>
              <button onClick={() => hacerSuper(userResult.id)}>Convertir en superadmin</button>
            </div>
          )}
        </div>
    </div>
  );
}
