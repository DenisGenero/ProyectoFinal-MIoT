
export default function BuscarImagenes({ fecha, handleFechaChange, handleSearchClick, imagenes }) {

return (
    <>
    <h3>Buscar imágenes por fecha</h3>
      <input type="date" value={fecha} onChange={handleFechaChange} />
      &nbsp;&nbsp;&nbsp;&nbsp;
      <button onClick={handleSearchClick}>Buscar</button>
      <div style={{ 
        display: "grid", 
        gridTemplateColumns: "repeat(2, 1fr)", 
        gap: "10px" 
      }}>
        {imagenes?.length === 0 ? (
          <p>No hay imágenes para esta fecha</p>
        ) : (
          imagenes.map((img, idx) => (
            <div key={idx} style={{ display: "inline-block", margin: "10px", textAlign: "center" }}>
              <img
                src={`http://localhost:8000/imagenes/${img.path_imagen}`}
                alt={`captura-${idx}`}
                style={{ 
                  width: "150px",
                  height: "auto",
                  border: "1px solid #ccc",
                  cursor: "pointer"
                }}
                onClick={() => window.open(`http://localhost:8000/imagenes/${img.path_imagen}`, "_blank")}
              />
              <div style={{ marginTop: "5px", fontSize: "14px" }}>
                {new Date(img.fecha).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" })}
              </div>
            </div>
          ))
        )}
      </div>
    </>
)}