import React, { useState, useEffect } from 'react';
import { gestionService } from '../../services/api';

const AdminDesignaciones = () => {
    const [partidos, setPartidos] = useState([]);
    const [arbitros, setArbitros] = useState([]);
    const [designaciones, setDesignaciones] = useState([]);
    const [disponibilidades, setDisponibilidades] = useState([]);
    const [loading, setLoading] = useState(true);
    
    // Formulario de creación
    const [formData, setFormData] = useState({ partido: '', arbitro: '', rol_asignado: 'ARBITRO_1' });
    const [msg, setMsg] = useState('');

    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {
        setLoading(true);
        try {
            const [resPartidos, resArbitros, resDesig, resDisp] = await Promise.all([
                gestionService.getPartidos(),
                gestionService.getArbitros(),
                gestionService.getDesignaciones(),
                gestionService.getDisponibilidades()
            ]);
            setPartidos(resPartidos.data);
            setArbitros(resArbitros.data);
            setDesignaciones(resDesig.data);
            setDisponibilidades(resDisp.data);
        } catch (err) {
            console.error(err);
            setMsg('Error al cargar datos.');
        }
        setLoading(false);
    };

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await gestionService.createDesignacion(formData);
            setMsg('Designación creada ✅ Se enviará push al árbitro.');
            setFormData({ partido: '', arbitro: '', rol_asignado: 'ARBITRO_1' });
            fetchData();
            setTimeout(() => setMsg(''), 4000);
        } catch (err) {
            setMsg('Error o designación duplicada ❌');
        }
    };

    const handleDelete = async (id) => {
        if (!window.confirm('¿Seguro de borrar esta designación?')) return;
        try {
            await gestionService.deleteDesignacion(id);
            setMsg('Designación borrada 🗑️');
            fetchData();
        } catch(err) {
            setMsg('Error borrando ❌');
        }
    };

    // Helper para saber si un arbitro esta ocupado en fecha de un partido
    const revisarDisponibilidad = (arbitroId, partidoId) => {
        if (!partidoId || !arbitroId) return null;
        const p = partidos.find(x => x.id.toString() === partidoId.toString());
        if (!p) return null;
        const pDate = new Date(p.date_time);
        
        // Buscar si reporto no disponibilidad
        const ocupado = disponibilidades.find(d => {
            if (d.arbitro.toString() !== arbitroId.toString() || d.is_available) return false;
            return pDate >= new Date(d.start_time) && pDate <= new Date(d.end_time);
        });
        
        return ocupado ? "⚠️ Reportó NO estar disponible" : "✅ Pareciera libre";
    };

    if (loading) return <div className="container"><p>Cargando módulo...</p></div>;

    return (
        <div className="container" style={{ paddingBottom: '3rem' }}>
            <header style={{ marginBottom: '2rem' }}>
                <h2 className="sport-font" style={{ fontSize: '1.8rem', marginBottom: '0.3rem' }}>
                    哨 Asignar Árbitros
                </h2>
                <p style={{ color: 'var(--text-muted)' }}>Vincula a los árbitros con los partidos programados.</p>
            </header>

            <form onSubmit={handleSubmit} className="glass-card" style={{ marginBottom: '2rem' }}>
                <h3 className="sport-font" style={{ fontSize: '1.2rem', marginBottom: '1rem' }}>➕ Crear Designación</h3>
                
                <div style={{ marginBottom: '1rem' }}>
                    <label style={{ display: 'block', fontSize: '0.8rem', color: 'var(--text-muted)' }}>Partido</label>
                    <select className="input-field" name="partido" value={formData.partido} onChange={handleChange} required>
                        <option value="">Seleccione partido...</option>
                        {partidos.map(p => (
                            <option key={p.id} value={p.id}>{p.title} - {new Date(p.date_time).toLocaleString()}</option>
                        ))}
                    </select>
                </div>

                <div style={{ marginBottom: '1rem' }}>
                    <label style={{ display: 'block', fontSize: '0.8rem', color: 'var(--text-muted)' }}>Árbitro</label>
                    <select className="input-field" name="arbitro" value={formData.arbitro} onChange={handleChange} required>
                        <option value="">Seleccione árbitro...</option>
                        {arbitros.map(a => {
                            const nameInfo = a.user_data ? `${a.user_data.first_name} ${a.user_data.last_name}` : a.id;
                            return <option key={a.id} value={a.id}>{nameInfo}</option>;
                        })}
                    </select>
                    {formData.arbitro && formData.partido && (
                        <small style={{ display: 'block', marginTop: '0.5rem', color: revisarDisponibilidad(formData.arbitro, formData.partido).includes('⚠️') ? '#f87171' : 'var(--accent)' }}>
                            {revisarDisponibilidad(formData.arbitro, formData.partido)}
                        </small>
                    )}
                </div>

                <div style={{ marginBottom: '1.5rem' }}>
                    <label style={{ display: 'block', fontSize: '0.8rem', color: 'var(--text-muted)' }}>Rol / Puesto</label>
                    <select className="input-field" name="rol_asignado" value={formData.rol_asignado} onChange={handleChange} required>
                        <option value="ARBITRO_1">Árbitro 1</option>
                        <option value="ARBITRO_2">Árbitro 2</option>
                        <option value="MESA">Mesa de Control</option>
                    </select>
                </div>

                <button type="submit" className="btn-primary" style={{ width: '100%' }}>Asignar</button>
                {msg && <p style={{ marginTop: '1rem', textAlign: 'center', color: 'var(--accent)' }}>{msg}</p>}
            </form>

            <div>
                <h3 className="sport-font" style={{ fontSize: '1.2rem', marginBottom: '1rem' }}>📋 Designaciones Actuales</h3>
                {designaciones.length === 0 ? <p style={{ color: 'var(--text-muted)' }}>No hay asignaciones.</p> : (
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.8rem' }}>
                        {designaciones.map(d => {
                            const p = partidos.find(x => x.id === d.partido);
                            const pTitle = p ? p.title : `Partido #${d.partido}`;
                            const a = arbitros.find(x => x.id === d.arbitro);
                            const aName = a && a.user_data ? `${a.user_data.first_name}` : `Arb #${d.arbitro}`;
                            
                            return (
                                <div key={d.id} className="glass-card" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '0.8rem 1rem' }}>
                                    <div>
                                        <h4 style={{ margin: 0, fontSize: '0.95rem' }}>{aName} como {d.rol_asignado}</h4>
                                        <p style={{ margin: 0, fontSize: '0.8rem', color: 'var(--text-muted)' }}>{pTitle} • Estado: {d.status}</p>
                                    </div>
                                    <button onClick={() => handleDelete(d.id)} style={{ background: 'none', border: '1px solid #f87171', color: '#f87171', padding: '0.3rem 0.6rem', borderRadius: '4px', cursor: 'pointer' }}>🗑️</button>
                                </div>
                            );
                        })}
                    </div>
                )}
            </div>
        </div>
    );
};

export default AdminDesignaciones;
