// src/components/UserPanel.jsx
import { useEffect, useState } from "react";
import { getUserInfo, actualizarUsuario, logout } from "../../services/auth.service";

export default function UsuarioPanel() {
  const [abierto, setAbierto] = useState(false);
  const [editando, setEditando] = useState(false);
  const [user, setUser] = useState(null);
  const [form, setForm] = useState({});

  // ---------- CARGA INICIAL ----------
  useEffect(() => {
    cargarUsuario();
  }, []);

  async function cargarUsuario() {
    try {
      const data = await getUserInfo();
      setUser(data);
      setForm({
        nombres: data.nombres || "",
        apellidos: data.apellidos || "",
        email: data.email || "",
        password: "",
      });
    } catch (e) {
        const errMsg = err.response?.data?.detail || "Ocurrió un error inesperado";
        throw new Error(errMsg)
      }
    }

  // ---------- HANDLERS ----------
  function handleEditar() {
    setEditando(true);
  }

  function handleInput(e) {
    setForm({
      ...form,
      [e.target.name]: e.target.value
    });
  }

  async function handleGuardar() {
    try {
      await actualizarUsuario(form);
      setEditando(false);
      cargarUsuario();
    } catch (e) {
      console.error(e);
    }
  }

  function handleLogout() {
    logout();
    window.location.reload();
  }

  // ---------- RENDER ----------
  return (
    <div style={{marginTop:"30%"}}>
      <h3>Perfil</h3>

      <button onClick={() => {
        //getUserInfo()
        setAbierto(!abierto)
        setEditando(false)}}
        className="btn-myuser">
        Mi usuario
      </button> <br /><br />

      {abierto && user && (
        <div >
          {!editando ? (
            <>
              <p><b>Nombre:</b> {user.nombres}</p>
              <p><strong>Apellido:</strong> {user.apellidos}</p>
              <p><strong>Email:</strong> {user.email}</p>
              <p><strong>Fecha alta: </strong> 
                {new Date(user.fecha_alta).toLocaleDateString("es-AR", {
                    day: "2-digit",
                    month: "2-digit",
                    year: "numeric",
                })}</p>
              <p><strong>Último acceso: </strong> <br />
                {new Date(user.ultimo_acceso).toLocaleString("es-AR", {
                    day: "2-digit",
                    month: "2-digit",
                    year: "numeric",
                    hour: "2-digit",
                    minute: "2-digit",
                    second: "2-digit",
                }).replace(",", " a las")}
            </p>

              <button onClick={handleEditar} className="btn-edit">
                Editar
              </button> &nbsp;&nbsp;
              <button onClick={() => setAbierto(!abierto)} className="btn-close">
                Ocultar
              </button><br /><br />
            </>
          ) : (
            <>
              <label><b>Nombre</b></label><br />
              <input
                name="nombres"
                value={form.nombres}
                onChange={handleInput}
              /><br /><br />

              <label><b>Apellido</b></label><br />
              <input
                name="apellidos"
                value={form.apellidos}
                onChange={handleInput}
              /><br /><br />

              <label><b>Email</b></label><br />
              <input
                name="email"
                value={form.email}
                onChange={handleInput}
              /><br /><br />

              <label><b>Contraseña</b></label><br />
              <input
                name="password"
                type="password"
                value={form.password}
                onChange={handleInput}
              /><br /><br />

              <button onClick={handleGuardar} className="btn-save">
                Guardar
              </button> &nbsp;&nbsp;
              <button onClick={() => setEditando(false)} className="btn-cancel">
                Cancelar
              </button><br /><br />
            </>
          )}
        </div>
      )}
      <button onClick={handleLogout} className="btn-logout">
        Cerrar sesión
      </button>
      <br />
      <br />
      <br />
    </div>
  );
}

