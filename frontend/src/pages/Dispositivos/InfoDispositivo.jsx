
export default function InfoDispositivo({dispositivo}) {
    
  return (
    <>
      <h2>{dispositivo?.nombre || "Sin nombre"}</h2>
      <p>Hora inicio: {dispositivo?.hora_inicio || "No configurada"}</p>
      <p>Hora fin: {dispositivo?.hora_fin || "No configurada"}</p>
      {dispositivo?.intervalo === null ? (
        <p>Intervalo: No configurado</p>
      ) : (
        <p>Intervalo: {dispositivo.intervalo} minutos</p>
      )}
    </>
  );
}