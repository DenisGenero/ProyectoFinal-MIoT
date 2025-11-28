import { useState } from "react";
import { updateDeviceAdminConfig } from "../../services/superadmin.service";

export default function DispositivoAdminEdit({ device, onCancel, onSaved }) {
    const [form, setForm] = useState({
    mac_address: device.mac_address || "",
    usuario_local: device.usuario_local || "",
    direccion_local: device.direccion_local || "",
    puerto_ssh: device.puerto_ssh || "",
    usuario_servidor: device.usuario_servidor || "",
    direccion_servidor: device.direccion_servidor || "",
    puerto_servidor: device.puerto_servidor || "",
  });

  const handleChange = (campo, valor) => {
    const numericFields = ["puerto_ssh", "puerto_servidor"];

    // si el campo es numérico:
    if (numericFields.includes(campo)) {
        // si está vacío → dejar null
        return setForm(prev => ({
        ...prev,
        [campo]: valor === "" ? null : parseInt(valor, 10)
        }));
    }

    setForm(prev => ({
        ...prev,
        [campo]: valor
    }));
  };

  const guardar = async () => {
    try {
      await updateDeviceAdminConfig(device.id, form);

      alert("Configuración actualizada correctamente");

      if (onSaved) onSaved();   // avisar al padre
    } catch (err) {
      alert("Error actualizando dispositivo");
      console.error(err);
    }
  };

  return (
    <div >

      <label>MAC:</label><br />
      <input type="text" value={form.mac_address ?? ""} onChange={(e) => handleChange("mac_address", e.target.value)}/><br />

      <label>Usuario local:</label><br />
      <input type="text" value={form.usuario_local ?? ""} onChange={(e) => handleChange("usuario_local", e.target.value)}/><br />

      <label>Dirección local:</label><br />
      <input type="text" value={form.direccion_local ?? ""} onChange={(e) => handleChange("direccion_local", e.target.value)}/><br />

      <label>Puerto SSH:</label><br />
      <input type="number" value={form.puerto_ssh ?? ""} onChange={(e) => handleChange("puerto_ssh", e.target.value)}/><br />

      <label>Usuario servidor:</label><br />
      <input type="text" value={form.usuario_servidor ?? ""} onChange={(e) => handleChange("usuario_servidor", e.target.value)}/><br />

      <label>Dirección servidor:</label><br />
      <input type="text" value={form.direccion_servidor ?? ""} onChange={(e) => handleChange("direccion_servidor", e.target.value)}/><br />

      <label>Puerto servidor:</label><br />
      <input type="number" value={form.puerto_servidor ?? ""} onChange={(e) => handleChange("puerto_servidor", e.target.value)}/><br />

      <button onClick={guardar}>Guardar</button>
      <button onClick={onCancel}>Cancelar</button>
    </div>
  );
}
