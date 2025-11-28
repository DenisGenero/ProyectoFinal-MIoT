import { useState } from "react";
import {
  getAllDevices,
  getUnconfiguredDevices,
  getDevicesByMac,
  getDevicesByUserEmail,
} from "../../services/superadmin.service";
import DispositivoAdminDetail from "./DispositivoAdminDetail";

export default function DispositivoList() {
  const [devices, setDevices] = useState([]);
  const [showMacInput, setShowMacInput] = useState(false);
  const [showUserInput, setShowUserInput] = useState(false);
  const [isEditing, setIsEditing] = useState(false);

  const [mac, setMac] = useState("");
  const [email, setEmail] = useState("");

  const [selectedDevice, setSelectedDevice] = useState(null);

  const buscarTodos = async () => {
    if (devices && devices.length > 0){
        setDevices([]);
        setSelectedDevice(null);
    } 
    else {
        const data = await getAllDevices();
        setDevices(data);
        setSelectedDevice(null);
    }
  };

  const buscarNoConfig = async () => {
    if (devices && devices.length > 0){
        setDevices([]);
        setSelectedDevice(null);
    } 
    else {
      const data = await getUnconfiguredDevices();
      setDevices(data);
      setSelectedDevice(null);
    }
  };

  const buscarPorMac = async () => {
    if (!mac) return;
    const data = await getDevicesByMac(mac);
    setDevices(data ? [data] : []);
    setSelectedDevice(null);
  };

  const buscarPorEmail = async () => {
    if (!email) return;
    const data = await getDevicesByUserEmail(email);
    setDevices(data);
    setSelectedDevice(null);
  };

  return (
    <div>
      <h2>Dispositivos</h2>

      {/* BOTONES PRINCIPALES */}
      <button onClick={buscarTodos}>Todos</button>
      <button onClick={buscarNoConfig}>No Configurados</button>
      <button onClick={() => { setShowMacInput(!showMacInput); setShowUserInput(false); }}>
        Buscar por MAC
      </button>
      <button onClick={() => { setShowUserInput(!showUserInput); setShowMacInput(false); }}>
        Buscar por Usuario
      </button>

      {/* INPUT MAC */}
      {showMacInput && (
        <div className="input-panel">
          <input
            type="text"
            placeholder="MAC"
            value={mac}
            onChange={(e) => setMac(e.target.value)}
          />
          <button onClick={buscarPorMac}>Buscar</button>
          <button onClick={() => setShowMacInput(false)}>Cancelar</button>
        </div>
      )}

      {/* INPUT EMAIL */}
      {showUserInput && (
        <div className="input-panel">
          <input
            type="text"
            placeholder="Email usuario"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <button onClick={buscarPorEmail}>Buscar</button>
          <button onClick={() => setShowUserInput(false)}>Cancelar</button>
        </div>
      )}

      {/* LISTADO DE DISPOSITIVOS */}
      {devices === null || devices.length === 0 ? (
        <p>No se encontraron dispositivos</p>
      ) : (
        <>
        <p>
          <strong>{devices.length}</strong> dispositivos encontrados
        </p>
      <ul>
        {devices.map((d) => (
          <li
            key={d.id}
            onClick={() => setSelectedDevice(d)}
            className="device-item"
          >
            <p><strong>ID:</strong> {d.id} <b>- Nombre:</b> {d.nombre}</p>
            {selectedDevice?.id === d.id && (
              <DispositivoAdminDetail 
                device={selectedDevice}
                onClose={() => { setSelectedDevice(null); setIsEditing(false); }}
                onEdit={() => setIsEditing(true)}
                isEditing={isEditing}
                onSaved={() => {
                  setIsEditing(false);
                  buscarNoConfig();
                }}
              />)}
          </li>
        ))}
      </ul>
      </>
      )}
    </div>
  );
}
