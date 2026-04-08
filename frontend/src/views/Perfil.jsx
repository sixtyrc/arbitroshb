import React, { useEffect, useState } from 'react';
import { gestionService } from '../services/api';

// Convierte una base64url string a Uint8Array (requerido por la API de Push)
function urlBase64ToUint8Array(base64String) {
    const padding = '='.repeat((4 - base64String.length % 4) % 4);
    const base64 = (base64String + padding).replace(/-/g, '+').replace(/_/g, '/');
    const rawData = window.atob(base64);
    const outputArray = new Uint8Array(rawData.length);
    for (let i = 0; i < rawData.length; ++i) {
        outputArray[i] = rawData.charCodeAt(i);
    }
    return outputArray;
}

const Perfil = () => {
    const [perfil, setPerfil] = useState({
        first_name: '', last_name: '', email: '', phone: '', cbu_alias: ''
    });
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [msg, setMsg] = useState({ text: '', type: '' });
    const [pushStatus, setPushStatus] = useState('idle'); // idle | loading | active | denied | unsupported

    useEffect(() => {
        fetchPerfil();
        checkPushStatus();
    }, []);

    const fetchPerfil = async () => {
        try {
            const res = await gestionService.getMiPerfil();
            setPerfil({
                first_name: res.data.user.first_name || '',
                last_name: res.data.user.last_name || '',
                email: res.data.user.email || '',
                phone: res.data.phone || '',
                cbu_alias: res.data.cbu_alias || ''
            });
        } catch (err) {
            console.error('Error al cargar perfil', err);
        } finally {
            setLoading(false);
        }
    };

    const checkPushStatus = () => {
        if (!('serviceWorker' in navigator) || !('PushManager' in window)) {
            setPushStatus('unsupported');
            return;
        }
        const perm = Notification.permission;
        if (perm === 'granted') setPushStatus('active');
        else if (perm === 'denied') setPushStatus('denied');
        else setPushStatus('idle');
    };

    const handleChange = (e) => {
        setPerfil({ ...perfil, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setSaving(true);
        setMsg({ text: '', type: '' });
        try {
            await gestionService.updateMiPerfil(perfil);
            setMsg({ text: '¡Perfil actualizado correctamente! ✅', type: 'success' });
        } catch (err) {
            setMsg({ text: 'Error al guardar. Intentá de nuevo. ❌', type: 'error' });
        } finally {
            setSaving(false);
        }
    };

    const handleActivarPush = async () => {
        if (pushStatus === 'denied') {
            alert('Bloqueaste las notificaciones en tu navegador. Habilitálas desde la configuración del sitio.');
            return;
        }
        setPushStatus('loading');
        try {
            // 1. Pedir la llave pública al backend
            const keyRes = await gestionService.getVapidKey();
            const vapidPublicKey = keyRes.data.public_key;

            // 2. Pedir permiso al browser y crear la suscripción
            const registration = await navigator.serviceWorker.ready;
            const subscription = await registration.pushManager.subscribe({
                userVisibleOnly: true,
                applicationServerKey: urlBase64ToUint8Array(vapidPublicKey)
            });

            // 3. Enviar la suscripción al backend para persistirla
            await gestionService.subscribePush(subscription.toJSON());

            setPushStatus('active');
        } catch (err) {
            console.error('Error al activar push:', err);
            if (Notification.permission === 'denied') {
                setPushStatus('denied');
            } else {
                setPushStatus('idle');
                alert('No se pudo activar. Asegurate de usar HTTPS o localhost.');
            }
        }
    };

    const pushLabel = {
        idle: { text: 'Activar Notificaciones', icon: '🔔', cls: 'btn-primary' },
        loading: { text: 'Activando...', icon: '⏳', cls: 'btn-primary' },
        active: { text: 'Notificaciones Activas', icon: '✅', cls: 'btn-success' },
        denied: { text: 'Bloqueadas por el sistema', icon: '🚫', cls: 'btn-danger' },
        unsupported: { text: 'No soportado', icon: '⚠️', cls: 'btn-disabled' },
    }[pushStatus];

    if (loading) return (
        <div className="container" style={{ textAlign: 'center', padding: '4rem 1rem' }}>
            <div style={{ fontSize: '2rem', marginBottom: '1rem' }}>⚙️</div>
            <p style={{ color: 'var(--text-muted)' }}>Cargando perfil...</p>
        </div>
    );

    return (
        <div className="container" style={{ paddingBottom: '3rem' }}>
            <header style={{ marginBottom: '2rem' }}>
                <h2 className="sport-font" style={{ fontSize: '1.8rem', marginBottom: '0.3rem' }}>
                    👤 Mi Perfil
                </h2>
                <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>
                    Mantené tus datos de contacto y pago actualizados.
                </p>
            </header>

            {/* Formulario de datos */}
            <form onSubmit={handleSubmit} className="glass-card" style={{ marginBottom: '1.5rem' }}>
                <h3 className="sport-font" style={{ fontSize: '1rem', marginBottom: '1.2rem', color: 'var(--text-muted)' }}>
                    DATOS PERSONALES
                </h3>

                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '1rem' }}>
                    <div>
                        <label style={{ display: 'block', marginBottom: '0.4rem', fontSize: '0.75rem', color: 'var(--text-muted)' }}>NOMBRE</label>
                        <input className="input-field" name="first_name" value={perfil.first_name} onChange={handleChange} required />
                    </div>
                    <div>
                        <label style={{ display: 'block', marginBottom: '0.4rem', fontSize: '0.75rem', color: 'var(--text-muted)' }}>APELLIDO</label>
                        <input className="input-field" name="last_name" value={perfil.last_name} onChange={handleChange} required />
                    </div>
                </div>

                <div style={{ marginBottom: '1rem' }}>
                    <label style={{ display: 'block', marginBottom: '0.4rem', fontSize: '0.75rem', color: 'var(--text-muted)' }}>EMAIL</label>
                    <input className="input-field" type="email" name="email" value={perfil.email} onChange={handleChange} required />
                </div>

                <div style={{ marginBottom: '1rem' }}>
                    <label style={{ display: 'block', marginBottom: '0.4rem', fontSize: '0.75rem', color: 'var(--text-muted)' }}>TELÉFONO / WHATSAPP</label>
                    <input className="input-field" name="phone" value={perfil.phone} onChange={handleChange} placeholder="+54 9 ..."/>
                </div>

                <div style={{ marginBottom: '1.5rem' }}>
                    <label style={{ display: 'block', marginBottom: '0.4rem', fontSize: '0.75rem', color: 'var(--accent)', fontWeight: 'bold' }}>
                        💳 CBU / ALIAS (PAGOS)
                    </label>
                    <input
                        className="input-field"
                        name="cbu_alias"
                        value={perfil.cbu_alias}
                        onChange={handleChange}
                        placeholder="Ej: nahuel.mp o 0000003100...0"
                        style={{ borderBottomColor: 'var(--accent)' }}
                    />
                    <small style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>
                        Acá te transferimos los honorarios de tus designaciones aceptadas.
                    </small>
                </div>

                {msg.text && (
                    <p style={{
                        marginBottom: '1rem',
                        textAlign: 'center',
                        fontSize: '0.88rem',
                        color: msg.type === 'success' ? 'var(--accent)' : '#f87171',
                        padding: '0.6rem',
                        borderRadius: '0.5rem',
                        background: msg.type === 'success' ? 'rgba(16, 185, 129, 0.1)' : 'rgba(248, 113, 113, 0.1)',
                    }}>
                        {msg.text}
                    </p>
                )}

                <button className="btn-primary" type="submit" disabled={saving}>
                    {saving ? '⏳ Guardando...' : '💾 Guardar Cambios'}
                </button>
            </form>

            {/* Sección de Notificaciones Push */}
            <section>
                <h3 className="sport-font" style={{ fontSize: '1rem', marginBottom: '1rem', color: 'var(--text-muted)' }}>
                    NOTIFICACIONES
                </h3>
                <div className="glass-card" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: '1rem' }}>
                    <div>
                        <p style={{ fontWeight: 'bold', fontSize: '0.95rem', marginBottom: '0.3rem' }}>
                            {pushLabel.icon} Notificaciones Push
                        </p>
                        <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                            {pushStatus === 'active'
                                ? 'Recibirás alertas al instante cuando te designen un partido.'
                                : pushStatus === 'denied'
                                ? 'Bloqueaste los permisos desde el navegador.'
                                : pushStatus === 'unsupported'
                                ? 'Tu navegador no soporta notificaciones push.'
                                : 'Activá para recibir avisos de nuevas designaciones en tiempo real.'
                            }
                        </p>
                    </div>
                    <button
                        onClick={handleActivarPush}
                        disabled={pushStatus === 'loading' || pushStatus === 'active' || pushStatus === 'unsupported'}
                        style={{
                            flexShrink: 0,
                            width: 'auto',
                            padding: '0.55rem 1.2rem',
                            fontSize: '0.82rem',
                            opacity: (pushStatus === 'active' || pushStatus === 'unsupported') ? 0.6 : 1,
                            cursor: (pushStatus === 'active' || pushStatus === 'unsupported') ? 'default' : 'pointer',
                            background: pushStatus === 'active' ? 'rgba(16, 185, 129, 0.2)' : undefined,
                            borderColor: pushStatus === 'active' ? 'var(--accent)' : undefined,
                        }}
                        className="btn-primary"
                    >
                        {pushLabel.text}
                    </button>
                </div>
            </section>
        </div>
    );
};

export default Perfil;
