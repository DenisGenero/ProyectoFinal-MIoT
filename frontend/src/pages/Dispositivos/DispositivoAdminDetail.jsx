import DispositivoAdminEdit from "./DispositivoAdminEdit";

export default function DispositivoAdminDetail({ device, onClose, onEdit, isEditing }) {
  if (!device) return null;

  // Si está editando → MOSTRAR formulario de edición
  if (isEditing) {
    return (
      <DispositivoAdminEdit 
        device={device}
        onCancel={onClose}
      />
    );
  }

  // Si NO está editando → MOSTRAR detalles
  return (
    <div className="device-detail">
      <p><strong>Comedero ID:</strong> {device.id_comedero}</p>
      {device.mac_address ? (
        <>
          <p><strong>MAC:</strong> {device.mac_address}</p>
          <p><strong>Usuario local:</strong> {device.usuario_local || "No configurado"}</p>
          <p><strong>Dirección local:</strong> {device.direccion_local || "No configurado"}</p>
          <p><strong>Puerto SSH:</strong> {device.puerto_ssh || "No configurado"}</p>
          <p><strong>Usuario servidor:</strong> {device.usuario_servidor || "No configurado"}</p>
          <p><strong>Dirección servidor:</strong> {device.direccion_servidor || "No configurado"}</p>
          <p><strong>Puerto servidor:</strong> {device.puerto_servidor || "No configurado"}</p>
          <p><strong>Estado:</strong> {device.estado ? "Activo" : "Inactivo"}</p>
        </>
      ) : (
        <p><strong>No configurado</strong></p>
      )}

      <button onClick={onEdit}>Editar</button>
      <button onClick={(e) => { 
        e.stopPropagation();
        onClose();
        }}>
        Cancelar
      </button>
    </div>
  );
}
