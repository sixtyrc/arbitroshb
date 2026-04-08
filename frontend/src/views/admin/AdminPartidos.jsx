import React, { useState, useEffect } from 'react';
import { gestionService } from '../../services/api';

const AdminPartidos = () => {
    const [partidos, setPartidos] = useState([]);
    const [categorias, setCategorias] = useState([]);
    const [loading, setLoading] = useState(true);
    const [formData, setFormData] = useState({ id: null, title: '', location: '', date_time: '', categoria: '' });
    const [isEditing, setIsEditing] = useState(false);
    const [msg, setMsg] = useState('');

    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {
        setLoading(true);
        try {
            const [resPartidos, resCategorias] = await Promise.all([
                gestionService.getPartidos(),
                gestionService.getCategorias()
            ]);
            setPartidos(resPartidos.data);
            setCategorias(resCategorias.data);
        } catch (err) {
            console.error(err);
            setMsg('Error cargando datos.');
        }
        setLoading(false);
    };

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            if (isEditing) {
                await gestionService.updatePartido(formData.id, formData);
                setMsg('Partido actualizado ✅');
            } else {
                await gestionService.createPartido(formData);
                setMsg('Partido creado ✅');
            }
            setFormData({ id: null, title: '', location: '', date_time: '', categoria: '' });
            setIsEditing(false);
            fetchData();
            setTimeout(() => setMsg(''), 3000);
        } catch (err) {
            setMsg('Error al guardar ❌');
        }
    };

    const handleEdit = (p) => {
        setIsEditing(true);
        // Formatear date_time para el input datetime-local
        let dt = '';
        if (p.date_time) {
            const dateObj = new Date(p.date_time);
            dt = new Date(dateObj.getTime() - dateObj.getTimezoneOffset() * 60000).toISOString().slice(0, 16);
        }
        setFormData({
            id: p.id,
            title: p.title,
            location: p.location,
            date_time: dt,
            categoria: p.categoria || ''
        });
        window.scrollTo(0, 0);
    };

    const handleDelete = async (id) => {
        if (!window.confirm('¿Seguro que deseas eliminar este partido?')) return;
        try {
            await gestionService.deletePartido(id);
            setMsg('Partido eliminado 🗑️');
            fetchData();
        } catch (err) {
            setMsg('Error eliminando ❌');
        }
    };

    if (loading) return <div className="container"><p>Cargando modulo...</p></div>;

    return (
        <div className="container" style={{ paddingBottom: '3rem' }}>
            <header style={{ marginBottom: '2rem' }}>
                <h2 className="sport-font" style={{ fontSize: '1.8rem', marginBottom: '0.3rem' }}>
                    🏆 Gestión de Partidos
                </h2>
                <p style={{ color: 'var(--text-muted)' }}>Crea, edita o elimina partidos del sistema.</p>
            </header>

            <form onSubmit={handleSubmit} className="glass-card" style={{ marginBottom: '2rem' }}>
                <h3 className="sport-font" style={{ fontSize: '1.2rem', marginBottom: '1rem' }}>
                    {isEditing ? '✏️ Editar Partido' : '➕ Nuevo Partido'}
                </h3>
                
                <div style={{ marginBottom: '1rem' }}>
                    <label style={{ display: 'block', fontSize: '0.8rem', color: 'var(--text-muted)' }}>Título del Partido</label>
                    <input className="input-field" name="title" value={formData.title} onChange={handleChange} required placeholder="Ej: Final Mayores..." />
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '1rem' }}>
                    <div>
                        <label style={{ display: 'block', fontSize: '0.8rem', color: 'var(--text-muted)' }}>Categoría</label>
                        <select className="input-field" name="categoria" value={formData.categoria} onChange={handleChange} required>
                            <option value="">Seleccione...</option>
                            {categorias.map(cat => (
                                <option key={cat.id} value={cat.id}>{cat.nombre}</option>
                            ))}
                        </select>
                    </div>
                    <div>
                        <label style={{ display: 'block', fontSize: '0.8rem', color: 'var(--text-muted)' }}>Fecha y Hora</label>
                        <input className="input-field" type="datetime-local" name="date_time" value={formData.date_time} onChange={handleChange} required />
                    </div>
                </div>

                <div style={{ marginBottom: '1.5rem' }}>
                    <label style={{ display: 'block', fontSize: '0.8rem', color: 'var(--text-muted)' }}>Ubicación / Cancha</label>
                    <input className="input-field" name="location" value={formData.location} onChange={handleChange} required placeholder="Sede..." />
                </div>

                <div style={{ display: 'flex', gap: '1rem' }}>
                    <button type="submit" className="btn-primary" style={{ flex: 1 }}>{isEditing ? 'Guardar Cambios' : 'Crear Partido'}</button>
                    {isEditing && (
                        <button type="button" className="btn-disabled" onClick={() => { setIsEditing(false); setFormData({ id: null, title: '', location: '', date_time: '', categoria: '' }) }} style={{ flex: 1 }}>Cancelar</button>
                    )}
                </div>
                {msg && <p style={{ marginTop: '1rem', textAlign: 'center', color: 'var(--accent)' }}>{msg}</p>}
            </form>

            <div>
                <h3 className="sport-font" style={{ fontSize: '1.2rem', marginBottom: '1rem' }}>📋 Próximos Partidos</h3>
                {partidos.length === 0 ? <p style={{ color: 'var(--text-muted)' }}>No hay partidos cargados.</p> : (
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                        {partidos.map(p => (
                            <div key={p.id} className="glass-card" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '1rem' }}>
                                <div>
                                    <h4 style={{ margin: 0, fontSize: '1rem' }}>{p.title}</h4>
                                    <p style={{ margin: 0, fontSize: '0.8rem', color: 'var(--text-muted)' }}>{new Date(p.date_time).toLocaleString()} • {p.location}</p>
                                </div>
                                <div style={{ display: 'flex', gap: '0.5rem' }}>
                                    <button onClick={() => handleEdit(p)} style={{ background: 'none', border: '1px solid var(--accent)', color: 'var(--accent)', padding: '0.3rem 0.6rem', borderRadius: '4px', cursor: 'pointer' }}>✏️</button>
                                    <button onClick={() => handleDelete(p.id)} style={{ background: 'none', border: '1px solid #f87171', color: '#f87171', padding: '0.3rem 0.6rem', borderRadius: '4px', cursor: 'pointer' }}>🗑️</button>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
};

export default AdminPartidos;
