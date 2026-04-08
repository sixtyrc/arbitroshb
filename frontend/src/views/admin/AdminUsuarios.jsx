import React, { useState, useEffect } from 'react';
import { gestionService } from '../../services/api';

const AdminUsuarios = () => {
    const [usuarios, setUsuarios] = useState([]);
    const [loading, setLoading] = useState(true);
    const [formData, setFormData] = useState({ id: null, username: '', password: '', email: '', first_name: '', last_name: '', role: 'ARBITRO' });
    const [isEditing, setIsEditing] = useState(false);
    const [msg, setMsg] = useState('');

    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {
        setLoading(true);
        try {
            const res = await gestionService.getUsers();
            setUsuarios(res.data);
        } catch (err) {
            console.error(err);
            setMsg('Error cargando usuarios.');
        }
        setLoading(false);
    };

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            let dataToSend = { ...formData };
            if (!dataToSend.password) {
                delete dataToSend.password; // Don't send empty password strings
            }
            if (isEditing) {
                await gestionService.updateUser(formData.id, dataToSend);
                setMsg('Usuario/Contraseña actualizado ✅');
            } else {
                await gestionService.createUser(dataToSend);
                setMsg('Usuario creado ✅');
            }
            setFormData({ id: null, username: '', password: '', email: '', first_name: '', last_name: '', role: 'ARBITRO' });
            setIsEditing(false);
            fetchData();
            setTimeout(() => setMsg(''), 3000);
        } catch (err) {
            setMsg('Error al guardar ❌ Revise que el usuario no exista.');
        }
    };

    const handleEdit = (u) => {
        setIsEditing(true);
        setFormData({
            id: u.id,
            username: u.username,
            password: '', // Blank by default, let admin type a new one
            email: u.email,
            first_name: u.first_name,
            last_name: u.last_name,
            role: u.role
        });
        window.scrollTo(0, 0);
    };

    if (loading) return <div className="container"><p>Cargando modulo de personal...</p></div>;

    return (
        <div className="container" style={{ paddingBottom: '3rem' }}>
            <header style={{ marginBottom: '2rem' }}>
                <h2 className="sport-font" style={{ fontSize: '1.8rem', marginBottom: '0.3rem' }}>
                    👥 Gestión de Árbitros
                </h2>
                <p style={{ color: 'var(--text-muted)' }}>Crea accesos y resetea contraseñas del personal colegiado.</p>
            </header>

            <form onSubmit={handleSubmit} className="glass-card" style={{ marginBottom: '2rem' }}>
                <h3 className="sport-font" style={{ fontSize: '1.2rem', marginBottom: '1rem' }}>
                    {isEditing ? '✏️ Editar Usuario' : '➕ Nuevo Usuario'}
                </h3>
                
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '1rem' }}>
                    <div>
                        <label className="input-label" style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Nombre</label>
                        <input className="input-field" name="first_name" value={formData.first_name} onChange={handleChange} required />
                    </div>
                    <div>
                        <label className="input-label" style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Apellido</label>
                        <input className="input-field" name="last_name" value={formData.last_name} onChange={handleChange} required />
                    </div>
                </div>

                <div style={{ marginBottom: '1rem' }}>
                    <label className="input-label" style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Email (Será su Identidad Principal)</label>
                    <input type="email" className="input-field" name="email" value={formData.email} onChange={handleChange} required />
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '1.5rem' }}>
                    <div>
                        <label className="input-label" style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Username (Nombre corto)</label>
                        <input className="input-field" name="username" value={formData.username} onChange={handleChange} required disabled={isEditing}/>
                    </div>
                    <div>
                        <label className="input-label" style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>{isEditing ? 'Nueva Clave (Opcional)' : 'Contraseña'}</label>
                        <input type="password" className="input-field" name="password" value={formData.password} onChange={handleChange} required={!isEditing} />
                    </div>
                </div>
                
                <div style={{ marginBottom: '1.5rem' }}>
                    <label className="input-label" style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Rol</label>
                    <select className="input-field" name="role" value={formData.role} onChange={handleChange} required>
                        <option value="ARBITRO">Árbitro de Campo / Mesa</option>
                        <option value="ADMIN">Asignador / Tesorero (ADMIN)</option>
                    </select>
                </div>

                <div style={{ display: 'flex', gap: '1rem' }}>
                    <button type="submit" className="btn-primary" style={{ flex: 1 }}>{isEditing ? 'Actualizar Perfil' : 'Dar de Alta'}</button>
                    {isEditing && (
                        <button type="button" className="btn-disabled" onClick={() => { setIsEditing(false); setFormData({ id: null, username: '', password: '', email: '', first_name: '', last_name: '', role: 'ARBITRO' }) }} style={{ flex: 1 }}>Cancelar</button>
                    )}
                </div>
                {msg && <p style={{ marginTop: '1rem', textAlign: 'center', color: 'var(--accent)' }}>{msg}</p>}
            </form>

            <div>
                <h3 className="sport-font" style={{ fontSize: '1.2rem', marginBottom: '1rem' }}>📋 Plantel Colegiados</h3>
                {usuarios.length === 0 ? <p style={{ color: 'var(--text-muted)' }}>No hay usuarios.</p> : (
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                        {usuarios.map(u => (
                            <div key={u.id} className="glass-card" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '1rem' }}>
                                <div>
                                    <h4 style={{ margin: 0, fontSize: '1rem' }}>{u.first_name} {u.last_name} {u.role === 'ADMIN' && '👑'}</h4>
                                    <p style={{ margin: 0, fontSize: '0.8rem', color: 'var(--text-muted)' }}>@{u.username} • {u.email}</p>
                                </div>
                                <button onClick={() => handleEdit(u)} style={{ background: 'none', border: '1px solid var(--accent)', color: 'var(--accent)', padding: '0.3rem 0.6rem', borderRadius: '4px', cursor: 'pointer' }}>⚙️ Ajustes</button>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
};

export default AdminUsuarios;
