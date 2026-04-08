import os

def create_admin_views():
    base_dir = os.path.join("d:\\", "Proyectos", "Arbitros", "frontend", "src", "views", "admin")
    os.makedirs(base_dir, exist_ok=True)

    files_content = {
        "AdminDashboard.jsx": """import React from 'react';
import { useNavigate } from 'react-router-dom';

const AdminDashboard = () => {
    const navigate = useNavigate();
    return (
        <div className="container" style={{ paddingBottom: '3rem' }}>
            <header style={{ marginBottom: '2rem' }}>
                <h2 className="sport-font" style={{ fontSize: '1.8rem', marginBottom: '0.3rem' }}>
                    👑 Panel de Control
                </h2>
                <p style={{ color: 'var(--text-muted)' }}>Gestión general de Árbitros, Partidos y Designaciones.</p>
            </header>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: '1rem' }}>
                <div className="glass-card" onClick={() => navigate('/admin/partidos')} style={{ cursor: 'pointer', textAlign: 'center' }}>
                    <h3 style={{ fontSize: '1.2rem', marginBottom: '0.5rem' }}>🏆 Partidos</h3>
                    <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Crear y editar calendario</p>
                </div>
                <div className="glass-card" onClick={() => navigate('/admin/designaciones')} style={{ cursor: 'pointer', textAlign: 'center' }}>
                    <h3 style={{ fontSize: '1.2rem', marginBottom: '0.5rem' }}>哨 Designaciones</h3>
                    <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Asignar árbitros y mesas</p>
                </div>
                <div className="glass-card" onClick={() => navigate('/admin/liquidaciones')} style={{ cursor: 'pointer', textAlign: 'center' }}>
                    <h3 style={{ fontSize: '1.2rem', marginBottom: '0.5rem' }}>💰 Liquidaciones</h3>
                    <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Exportar excel de pagos</p>
                </div>
            </div>
        </div>
    );
};

export default AdminDashboard;
""",
        "AdminPartidos.jsx": """import React from 'react';

const AdminPartidos = () => {
    return (
        <div className="container" style={{ paddingBottom: '3rem' }}>
            <header style={{ marginBottom: '2rem' }}>
                <h2 className="sport-font" style={{ fontSize: '1.8rem', marginBottom: '0.3rem' }}>
                    🏆 Gestión de Partidos
                </h2>
                <p style={{ color: 'var(--text-muted)' }}>Aquí irá el CRUD para cargar nuevos partidos en el sistema.</p>
            </header>
            <div className="glass-card">
                <p>Módulo de partidos en construcción (Fase 2)...</p>
            </div>
        </div>
    );
};

export default AdminPartidos;
""",
        "AdminDesignaciones.jsx": """import React from 'react';

const AdminDesignaciones = () => {
    return (
        <div className="container" style={{ paddingBottom: '3rem' }}>
            <header style={{ marginBottom: '2rem' }}>
                <h2 className="sport-font" style={{ fontSize: '1.8rem', marginBottom: '0.3rem' }}>
                    哨 Asignar Árbitros
                </h2>
                <p style={{ color: 'var(--text-muted)' }}>Supervisa la disponibilidad de los árbitros y guárdalos en las designaciones de los partidos creados.</p>
            </header>
            <div className="glass-card">
                <p>Módulo de designaciones en construcción (Fase 2)...</p>
            </div>
        </div>
    );
};

export default AdminDesignaciones;
"""
    }

    for filename, content in files_content.items():
        filepath = os.path.join(base_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Generado {filename} en {filepath}")

if __name__ == "__main__":
    create_admin_views()
