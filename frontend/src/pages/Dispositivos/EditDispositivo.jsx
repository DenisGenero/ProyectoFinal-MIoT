
export default function EditarDispositivo({ editForm, handleFormChange, handleUpdate, onCancel }) {
  return (
    <form onSubmit={handleUpdate}>
      <label>
        Nombre: &nbsp;&nbsp;
        <input type="text" name="nombre" value={editForm.nombre} onChange={handleFormChange} />
      </label>
      <br /><br />
      <label>
        Hora inicio: &nbsp;&nbsp;
        <input type="time" name="hora_inicio" value={editForm.hora_inicio} onChange={handleFormChange} />
      </label>
      <br /><br />
      <label>
        Hora fin: &nbsp;&nbsp;
        <input type="time" name="hora_fin" value={editForm.hora_fin} onChange={handleFormChange} />
      </label>
      <br /><br />
      <label>
        Intervalo (min): &nbsp;&nbsp;
        <input type="number" name="intervalo" value={editForm.intervalo} onChange={handleFormChange} />
      </label>
      <br /><br />
      <button type="submit">Guardar cambios</button>
      <button type="button" onClick={onCancel}>
        Cancelar
      </button>
    </form>
  );
}
