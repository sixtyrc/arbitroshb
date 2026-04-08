import React, { useState, useEffect } from 'react';
import { gestionService } from '../../services/api';

const AdminLiquidaciones = () => {
    const [filtros, setFiltros] = useState({
        mes: '',
        fecha_inicio: '',
        fecha_fin: '',
        partido_id: ''
    });
    const [partidos, setPartidos] = useState([]);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        const fetchPartidos = async () => {
            try {
                const res = await gestionService.getPartidos();
                setPartidos(res.data);
            } catch (err) {
                console.error("Error cargando partidos");
            }
        };
        fetchPartidos();
    }, []);

    const handleDownload = async () => {
        setLoading(true);
        try {
            // Limpia keys vacios
            const filteredParams = Object.fromEntries(Object.entries(filtros).filter(([_, v]) => v !== ''));
            const response = await gestionService.downloadLiquidaciones(filteredParams);
            
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', `Liquidacion_Filtros.xlsx`);
            document.body.appendChild(link);
            link.click();
            link.parentNode.removeChild(link);
        } catch (err) {
            console.error('Error al descargar:', err);
            alert('Error al descargar el Excel');
        }
        setLoading(false);
    };

    const handleChange = (e) => {
        setFiltros({ ...filtros, [e.target.name]: e.target.value });
    };

    const clearFilters = () => {
        setFiltros({ mes: '', fecha_inicio: '', fecha_fin: '', partido_id: '' });
    };

    return (
        <div className="container" style={{ paddingBottom: '3rem' }}>
            <header style={{ marginBottom: '2rem' }}>
                <h2 className="sport-font" style={{ fontSize: '1.8rem', marginBottom: '0.3rem' }}>
                    💰 Reporte de Liquidaciones
                </h2>
                <p style={{ color: 'var(--text-muted)' }}>Exporta la liquidación con filtros flexibles por partido, rango de tiempo o mes.</p>
            </header>

            <div className="glass-card" style={{ marginBottom: '2rem' }}>
                <h3 className="sport-font" style={{ fontSize: '1.2rem', marginBottom: '1rem' }}>Filtros</h3>
                
                <div style={{ marginBottom: '1rem' }}>
                    <label style={{ display: 'block', fontSize: '0.8rem', color: 'var(--text-muted)' }}>Filtrar por Partido Específico</label>
                    <select className="input-field" name="partido_id" value={filtros.partido_id} onChange={handleChange}>
                        <option value="">-- Todos los partidos --</option>
                        {partidos.map(p => (
                            <option key={p.id} value={p.id}>{p.title} - {new Date(p.date_time).toLocaleDateString()}</option>
                        ))}
                    </select>
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: 'minmax(0, 1fr) minmax(0, 1fr)', gap: '1rem', marginBottom: '1rem' }}>
                    <div>
                        <label style={{ display: 'block', fontSize: '0.8rem', color: 'var(--text-muted)' }}>Fecha Inicio</label>
                        <input className="input-field" type="date" name="fecha_inicio" value={filtros.fecha_inicio} onChange={handleChange} disabled={!!filtros.mes} />
                    </div>
                    <div>
                        <label style={{ display: 'block', fontSize: '0.8rem', color: 'var(--text-muted)' }}>Fecha Fin</label>
                        <input className="input-field" type="date" name="fecha_fin" value={filtros.fecha_fin} onChange={handleChange} disabled={!!filtros.mes} />
                    </div>
                </div>

                <div style={{ marginBottom: '1.5rem', textAlign: 'center' }}>
                    <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)', display: 'block', marginBottom: '0.5rem' }}>--- Ó BÚSQUEDA RÁPIDA POR MES ---</span>
                    <input className="input-field" type="month" name="mes" value={filtros.mes} onChange={handleChange} disabled={!!filtros.fecha_inicio || !!filtros.fecha_fin} />
                </div>

                <div style={{ display: 'flex', gap: '0.5rem' }}>
                    <button onClick={clearFilters} className="btn-disabled" style={{ flex: 1 }}>Limpiar Filtros</button>
                    <button onClick={handleDownload} disabled={loading} className="btn-primary" style={{ flex: 2 }}>
                        {loading ? '⏳ Generando Excel...' : '📊 Descargar Excel'}
                    </button>
                </div>
            </div>
        </div>
    );
};

export default AdminLiquidaciones;
