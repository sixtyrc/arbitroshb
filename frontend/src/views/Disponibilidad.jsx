import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { gestionService } from '../services/api';

const Disponibilidad = () => {
  const [fecha, setFecha] = useState('');
  const [horaInicio, setHoraInicio] = useState('08:00');
  const [horaFin, setHoraFin] = useState('22:00');
  const [misDisponibilidades, setMisDisponibilidades] = useState([]);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    cargarDisponibilidad();
  }, []);

  const cargarDisponibilidad = async () => {
    try {
      const res = await gestionService.getDisponibilidades();
      setMisDisponibilidades(res.data);
    } catch (err) {
      console.error("Error cargando disponibilidad", err);
    }
  };

  const handleSave = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      // Combinar fecha y hora para el formato Django ISO
      const start = `${fecha}T${horaInicio}:00Z`;
      const end = `${fecha}T${horaFin}:00Z`;
      
      await gestionService.addDisponibilidad({
          arbitro: 1, // Nota: Se debería obtener del perfil del usuario logueado en prod
          start_time: start,
          end_time: end,
          is_available: true
      });
      alert("¡Disponibilidad guardada!");
      setFecha('');
      cargarDisponibilidad();
    } catch (err) {
      alert("Error al guardar. Verificá los datos.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <header style={{ marginBottom: '2rem', display: 'flex', alignItems: 'center', gap: '1rem' }}>
        <button onClick={() => navigate(-1)} style={{ background: 'none', border: 'none', color: 'white', fontSize: '1.5rem' }}>←</button>
        <h2 className="sport-font">Mi Disponibilidad</h2>
      </header>

      <div className="glass-card" style={{ marginBottom: '2rem' }}>
        <h3 className="sport-font" style={{ fontSize: '1rem', marginBottom: '1.5rem', color: 'var(--secondary)' }}>Nuevo Rango Libre</h3>
        <form onSubmit={handleSave}>
          <div className="input-group">
            <label>Fecha</label>
            <input type="date" value={fecha} onChange={(e) => setFecha(e.target.value)} required />
          </div>
          <div style={{ display: 'flex', gap: '1rem' }}>
            <div className="input-group" style={{ flex: 1 }}>
              <label>Desde</label>
              <input type="time" value={horaInicio} onChange={(e) => setHoraInicio(e.target.value)} required />
            </div>
            <div className="input-group" style={{ flex: 1 }}>
              <label>Hasta</label>
              <input type="time" value={horaFin} onChange={(e) => setHoraFin(e.target.value)} required />
            </div>
          </div>
          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? 'Guardando...' : 'Confirmar Disponibilidad'}
          </button>
        </form>
      </div>

      <section>
        <h3 className="sport-font" style={{ fontSize: '1rem', marginBottom: '1rem' }}>Mis Cargas Actuales</h3>
        {misDisponibilidades.length === 0 ? (
          <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>No tenés rangos cargados.</p>
        ) : (
          misDisponibilidades.map(d => (
            <div key={d.id} className="glass-card" style={{ padding: '1rem', marginBottom: '0.5rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <p style={{ fontWeight: 'bold' }}>{new Date(d.start_time).toLocaleDateString()}</p>
                <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                  {new Date(d.start_time).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})} - 
                  {new Date(d.end_time).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
                </p>
              </div>
              <span style={{ color: 'var(--accent)', fontSize: '0.8rem', fontWeight: 'bold' }}>LIBRE</span>
            </div>
          ))
        )}
      </section>
    </div>
  );
};

export default Disponibilidad;
