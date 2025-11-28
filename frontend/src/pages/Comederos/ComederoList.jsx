// src/pages/Tambos/ComederoList.jsx
import { Link } from "react-router-dom";

export default function ComederoList({ comederos }) {
  return (
    <>
      <h3>Comederos</h3>
      {comederos.length === 0 ? (
        <p>No hay comederos asociados</p>
      ) : (
        <ul>
          <p>Haga clic sobre el comedero al que desee entrar</p>

          {comederos.map((c) => (
            <li key={c.id} className="items">
              <Link to={`/comederos/${c.id}`} className="items">{c.nombre}</Link>
            </li>
          ))}
        </ul>
      )}
    </>
  );
}
