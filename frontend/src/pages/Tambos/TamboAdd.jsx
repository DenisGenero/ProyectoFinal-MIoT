// src/pages/Tambos/AddTambo.jsx
import React, { useState } from "react";
import { createTambo } from "../../services/tambo.service";

export default function AddTambo({ onTamboCreated, onCancel }) {
    const [nombre, setNombre] = useState("");
    const [descripcion, setDescripcion] = useState("");
    const [ubicacion, setUbicacion] = useState("");
    const [error, setError] = useState("");
    const [isSubmitting, setIsSubmitting] = useState(false);

    const handleCreate = async (e) => {
        e.preventDefault();
        setError("");
        setIsSubmitting(true);
        
        try {
            await createTambo(nombre, descripcion, ubicacion);
            setNombre("");
            setDescripcion("");
            setUbicacion("");
            
            if (onTamboCreated) {
                onTamboCreated(); 
            }
        } catch (err) {
            setError(err.message || "Error al crear el tambo.");
        } finally {
            setIsSubmitting(false);
            if (onCancel) {
                 onCancel();
            }
        }
    };

    return (
        <form onSubmit={handleCreate}>
            <h3>Crear un nuevo tambo</h3>
            {error && <p style={{ color: "red" }}>{error}</p>}
            
            <input
                type="text"
                placeholder="Nombre"
                value={nombre}
                onChange={(e) => setNombre(e.target.value)}
                required
                disabled={isSubmitting}
            />
            <br /><br />
            <input
                type="text"
                placeholder="Descripción"
                value={descripcion}
                onChange={(e) => setDescripcion(e.target.value)}
                disabled={isSubmitting}
            />
            <br /><br />
            <input
                type="text"
                placeholder="Ubicación"
                value={ubicacion}
                onChange={(e) => setUbicacion(e.target.value)}
                required
                disabled={isSubmitting}
            />
            <br /><br />
            
            <button style={{backgroundColor:"green"}}
                className="boton-crear" 
                type="submit" 
                disabled={isSubmitting}
            >
                {isSubmitting ? "Creando..." : "+ Crear"}
            </button> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            
            <button style={{backgroundColor:"red"}}
                type="button" 
                onClick={onCancel} // Usa el prop onCancel
                disabled={isSubmitting}
            >
                X Cancelar
            </button>
        </form>
    );
}