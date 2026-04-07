import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { gestionService } from '../services/api';

const Dashboard = () => {
  const [designaciones, setDesignaciones] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const res = await gestionService.getDesignaciones();
      setDesignaciones(res.data);
    } catch (err) {
      console.error("Error cargando dashboard", err);
    } finally {
      setLoading(false);
    }
  };

  const statusColor = (status) => {
    if (status === 'ACCEPTED') return 'var(--accent)';
    if (status === 'REJECTED') return 'var(--error)';
    return 'var(--secondary)';
  };

  return (
    <div className="container" style={{ paddingBottom: '5rem' }}>
      <header style={{ marginBottom: '2rem' }}>
        <h2 className="sport-font" style={{ fontSize: '1.8rem' }}>¡Hola, Árbitro!</h2>
        <p style={{ color: 'var(--text-muted)' }}>Tenés {designaciones.length} partidos en tu agenda.</p>
      </header>

      <section>
        <h3 className="sport-font" style={{ marginBottom: '1rem', fontSize: '1.2rem', color: 'var(--secondary)' }}>
          Designaciones Recientes
        </h3>

        {loading ? (
          <p>Cargando cancha...</p>
        ) : designaciones.length === 0 ? (
          <div className="glass-card" style={{ textAlign: 'center', padding: '3rem' }}>
            <p>No tenés partidos asignados por ahora.</p>
          </div>
        ) : (
          designaciones.map(item => (
            <div key={item.id} className="glass-card" style={{ marginBottom: '1rem', position: 'relative' }}>
               <div style={{ 
                position: 'absolute', top: '1rem', right: '1rem', 
                background: statusColor(item.status), 
                padding: '2px 10px', borderRadius: '20px', fontSize: '0.7rem', fontWeight: 'bold' 
              }}>
                {item.status === 'PENDING' ? 'PENDIENTE' : item.status}
              </div>

              <h4 style={{ fontSize: '1.1rem', marginBottom: '0.5rem' }}>{item.partido_detail.title}</h4>
              <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '1rem' }}>
                <p>📍 {item.partido_detail.location}</p>
                <p>📅 {new Date(item.partido_detail.date_time).toLocaleString()}</p>
                <p>🏅 Rol: {item.rol_asignado === 'MESA' ? 'Mesa de Control' : 'Árbitro'}</p>
              </div>

              <div style={{ 
                background: 'rgba(16, 185, 129, 0.1)', 
                border: '1px solid var(--accent)', 
                borderRadius: '10px', padding: '0.8rem', 
                textAlign: 'center', marginBottom: '1rem' 
              }}>
                <span style={{ fontSize: '0.8rem', color: 'var(--accent)', fontWeight: 'bold' }}>HONORARIO ESTIMADO:</span>
                <p style={{ fontSize: '1.2rem', fontWeight: 'bold', color: 'var(--accent)' }}>
                  ${new Intl.NumberFormat('es-AR').format(item.monto_honorario)}
                </p>
              </div>

              {item.status === 'PENDING' && (
                <div style={{ display: 'flex', gap: '1rem', marginTop: '1.5rem' }}>
                  <button className="btn-primary" style={{ padding: '0.6rem', fontSize: '0.9rem' }}>Aceptar</button>
                  <button className="btn-primary" style={{ padding: '0.6rem', background: 'transparent', border: '1px solid var(--error)', color: 'var(--error)', fontSize: '0.9rem' }}>
                    Rechazar
                  </button>
                </div>
              )}
            </div>
          ))
        )}
      </section>

      {/* Botón Flotante de Disponibilidad */}
      <button 
        className="btn-primary" 
        onClick={() => navigate('/disponibilidad')}
        style={{ 
        position: 'fixed', bottom: '5rem', right: '1rem', width: 'auto', 
        borderRadius: '50px', boxShadow: '0 4px 20px rgba(0,0,0,0.5)', 
        padding: '1rem 1.5rem' 
      }}>
        ➕ Cargar Disponibilidad
      </button>
    </div>
  );
};

export default Dashboard;
