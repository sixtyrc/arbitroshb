import os

def update_views_py():
    path = r"d:\Proyectos\Arbitros\gestion\views.py"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    old_view = """class LiquidacionesExcelView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        # Obtener parámetros de filtro opcionales
        mes = request.query_params.get('mes')    # formato: YYYY-MM
        aceptadas_only = request.query_params.get('aceptadas', 'true').lower() == 'true'

        designaciones = Designacion.objects.select_related(
            'arbitro__user', 'partido__categoria__grupo'
        ).all()

        if aceptadas_only:
            designaciones = designaciones.filter(status='ACCEPTED')
        if mes:
            try:
                year, month = mes.split('-')
                designaciones = designaciones.filter(
                    partido__date_time__year=int(year),
                    partido__date_time__month=int(month)
                )
            except ValueError:
                pass"""
    
    new_view = """class LiquidacionesExcelView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        # Filtros Dinámicos
        mes = request.query_params.get('mes')
        partido_id = request.query_params.get('partido_id')
        fecha_inicio = request.query_params.get('fecha_inicio')
        fecha_fin = request.query_params.get('fecha_fin')
        aceptadas_only = request.query_params.get('aceptadas', 'true').lower() == 'true'

        designaciones = Designacion.objects.select_related(
            'arbitro__user', 'partido__categoria__grupo'
        ).all()

        if aceptadas_only:
            designaciones = designaciones.filter(status='ACCEPTED')
        
        if partido_id:
            designaciones = designaciones.filter(partido_id=partido_id)
        
        if fecha_inicio:
            try:
                designaciones = designaciones.filter(partido__date_time__gte=fecha_inicio)
            except Exception:
                pass
        
        if fecha_fin:
            try:
                # Agregamos tiempo a fecha_fin si es solo YYYY-MM-DD para que tome final del dia
                if len(fecha_fin) == 10:
                    fecha_fin += " 23:59:59"
                designaciones = designaciones.filter(partido__date_time__lte=fecha_fin)
            except Exception:
                pass

        if mes and not (fecha_inicio or fecha_fin):
            try:
                year, month = mes.split('-')
                designaciones = designaciones.filter(
                    partido__date_time__year=int(year),
                    partido__date_time__month=int(month)
                )
            except ValueError:
                pass"""

    content = content.replace(old_view, new_view)
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated views.py LiquidacionesExcelView")

def update_api_js():
    path = r"d:\Proyectos\Arbitros\frontend\src\services\api.js"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    old_func = "downloadLiquidaciones: (mes) => api.get(`/liquidaciones/excel/?mes=${mes || ''}`, { responseType: 'blob' }),"
    new_func = "downloadLiquidaciones: (params) => api.get('/liquidaciones/excel/', { params, responseType: 'blob' }),"
    
    if old_func in content:
        content = content.replace(old_func, new_func)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print("Updated api.js downloadLiquidaciones")

def update_admin_liquidaciones_jsx():
    path = r"d:\Proyectos\Arbitros\frontend\src\views\admin\AdminLiquidaciones.jsx"
    jsx = """import React, { useState, useEffect } from 'react';
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
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(jsx)
    print("Updated AdminLiquidaciones.jsx")

if __name__ == "__main__":
    update_views_py()
    update_api_js()
    update_admin_liquidaciones_jsx()
    print("Update filters script completed!")
