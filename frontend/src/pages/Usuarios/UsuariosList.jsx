// src/pages/Usuarios/UsuarioList.jsx
import { useState } from "react";
import { desvincularUsuarioDeTambo, actualizarRolEnTambo } from "../../services/tambo.service";
//import AddUser from "./AddUser";


export default function UsuarioList({ tambo, roles, onTamboUpdate }) {
    const [selectedUser, setSelectedUser] = useState(null);

    const handleBajaUsuario = async (userId, tamboId) => {
        if (window.confirm("¿Seguro que desea desvincular este usuario del tambo?")) {
            try {
                await desvincularUsuarioDeTambo(userId, tamboId);
                onTamboUpdate();
                setSelectedUser(null);
            } catch (err) {
                alert("Error al dar de baja al usuario: " + err);
            }
        }
    };

    const handleChangeRol = async (userId, tamboId, nuevoRolId) => {
        try {
            await actualizarRolEnTambo(userId, tamboId, nuevoRolId); // tu endpoint
            onTamboUpdate();
        } catch (err) {
            alert("Error al actualizar el rol:" + err);
        }
    };

    if (!tambo || !tambo.usuarios) {
        return null;
    }

    return (
        <>
            <h3>Usuarios</h3>
            <p>Haga clic sobre un usuario si desea desvincularlo o modificar su rol</p>
            <ul> {tambo.usuarios.map((u) => (
                <li
                    key={u.usuario.id}
                    onClick={() => setSelectedUser(selectedUser?.usuario.id === u.usuario.id ? null : u)}
                    className="items"
                >
                    {u.usuario.nombres} {u.usuario.apellidos} → {u.rol?.nombre}
                    {selectedUser?.usuario.id === u.usuario.id && (
                        <div>
                            <p style={{ marginBottom: "0.1%", marginTop: "0.5%" }}><b>Mail: </b> {u.usuario.email}</p>
                            <label>
                                <b>Rol:</b>&nbsp;&nbsp;
                                <select
                                    value={u.rol?.id || ""}
                                    onChange={(e) => handleChangeRol(u.usuario.id, tambo.id, e.target.value)}
                                    onClick={(e) => e.stopPropagation()}
                                >
                                    {roles.map((r) => (
                                        <option key={r.id} value={r.id}>{r.nombre}</option>
                                    ))}
                                </select>
                            </label> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                            <button
                                style={{ marginTop: "0.4rem", background: "red", border: "none", borderRadius: "4px", padding: "0.3rem 0.6rem" }}
                                onClick={() => handleBajaUsuario(u.usuario.id, tambo.id)}
                            >
                                Dar de baja
                            </button> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                            <button
                                style={{ marginTop: "0.4rem", background: "#646cff", border: "none", borderRadius: "4px", padding: "0.3rem 0.6rem" }}
                                onClick={() => setSelectedUser(null)}
                            >
                                Ocultar
                            </button>
                        </div>
                    )}
                </li>))}
            </ul>
        </>
    );
}

