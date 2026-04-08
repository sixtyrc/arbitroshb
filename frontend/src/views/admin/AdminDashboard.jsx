import React from 'react';
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
