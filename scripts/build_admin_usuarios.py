import os

def update_serializers():
    path = r"d:\Proyectos\Arbitros\gestion\serializers.py"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    new_serializer = """class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name', 'role']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = CustomUser(**validated_data)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance"""

    if "def create(self, validated_data):" not in content and "password = serializers.CharField" not in content:
        import re
        content = re.sub(
            r"class UserSerializer\(serializers\.ModelSerializer\):\n    class Meta:\n        model = CustomUser\n        fields = \['id', 'username', 'email', 'first_name', 'last_name', 'role'\]",
            new_serializer,
            content,
            count=1
        )
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print("Updated UserSerializer to support password hashing.")

def update_api_js():
    path = r"d:\Proyectos\Arbitros\frontend\src\services\api.js"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    if "getUsers:" not in content:
        new_methods = """  getUsers: () => api.get('/users/'),
  createUser: (data) => api.post('/users/', data),
  updateUser: (id, data) => api.patch(`/users/${id}/`, data),
"""
        content = content.replace(
            "getArbitros: () => api.get('/arbitros/'),",
            "getArbitros: () => api.get('/arbitros/'),\n" + new_methods
        )
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print("Updated api.js with users endpoints")

def update_admin_usuarios_jsx():
    path = r"d:\Proyectos\Arbitros\frontend\src\views\admin\AdminUsuarios.jsx"
    jsx = """import React, { useState, useEffect } from 'react';
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
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(jsx)
    print("Updated AdminUsuarios.jsx")

def update_app_jsx():
    path = r"d:\Proyectos\Arbitros\frontend\src\App.jsx"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    if "AdminUsuarios" not in content:
        content = content.replace(
            "import AdminLiquidaciones from './views/admin/AdminLiquidaciones';",
             "import AdminLiquidaciones from './views/admin/AdminLiquidaciones';\nimport AdminUsuarios from './views/admin/AdminUsuarios';"
        )
        content = content.replace(
            '<Route path="/admin/partidos" element={<AdminPartidos />} />',
            '<Route path="/admin/partidos" element={<AdminPartidos />} />\n          <Route path="/admin/usuarios" element={<AdminUsuarios />} />'
        )
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print("Updated App.jsx with Usuarios route")

def update_admin_dashboard():
    path = r"d:\Proyectos\Arbitros\frontend\src\views\admin\AdminDashboard.jsx"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    new_card = """                <div className="glass-card" onClick={() => navigate('/admin/usuarios')} style={{ cursor: 'pointer', textAlign: 'center' }}>
                    <h3 style={{ fontSize: '1.2rem', marginBottom: '0.5rem' }}>👥 Plantel</h3>
                    <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Cuentas y Claves</p>
                </div>"""
                
    if "/admin/usuarios" not in content:
        content = content.replace(
            "</p>\n                </div>",
            "</p>\n                </div>\n" + new_card
        )
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print("Updated AdminDashboard.jsx with Usuarios portal")

def add_micro_animations():
    path = r"d:\Proyectos\Arbitros\frontend\src\index.css"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    anim_css = """
/* ---- Micro Animations ---- */
@keyframes shimmer {
  0% { background-position: -1000px 0; }
  100% { background-position: 1000px 0; }
}

.skeleton {
  animation: shimmer 2s infinite linear;
  background: linear-gradient(to right, var(--surface) 4%, #334155 25%, var(--surface) 36%);
  background-size: 1000px 100%;
}

.page-transition {
  animation: slideFadeIn 0.4s ease-out forwards;
}

@keyframes slideFadeIn {
  0% { opacity: 0; transform: translateY(10px); }
  100% { opacity: 1; transform: translateY(0); }
}
"""
    if "Micro Animations" not in content:
        with open(path, "a", encoding="utf-8") as f:
            f.write(anim_css)
        print("Updated index.css with animations")

if __name__ == "__main__":
    update_serializers()
    update_api_js()
    update_admin_usuarios_jsx()
    update_app_jsx()
    update_admin_dashboard()
    add_micro_animations()
    print("Build step for Admin Usuarios and Animations completed!")
