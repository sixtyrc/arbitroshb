import os

def update_api_js():
    # Only need downloadLiquidaciones which is already there
    pass

def update_admin_liquidaciones_jsx():
    path = r"d:\Proyectos\Arbitros\frontend\src\views\admin\AdminLiquidaciones.jsx"
    jsx = """import React, { useState } from 'react';
import { gestionService } from '../../services/api';

const AdminLiquidaciones = () => {
    const [mes, setMes] = useState('');
    const [loading, setLoading] = useState(false);

    const handleDownload = async () => {
        setLoading(true);
        try {
            const response = await gestionService.downloadLiquidaciones(mes);
            // Create blob link to download
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', `Liquidacion_${mes || 'completa'}.xlsx`);
            document.body.appendChild(link);
            link.click();
            link.parentNode.removeChild(link);
        } catch (err) {
            console.error('Error al descargar:', err);
            alert('Error al descargar el Excel');
        }
        setLoading(false);
    };

    return (
        <div className="container" style={{ paddingBottom: '3rem' }}>
            <header style={{ marginBottom: '2rem' }}>
                <h2 className="sport-font" style={{ fontSize: '1.8rem', marginBottom: '0.3rem' }}>
                    💰 Liquidaciones
                </h2>
                <p style={{ color: 'var(--text-muted)' }}>Exporta la consolidación de honorarios pagaderos a formato Excel.</p>
            </header>

            <div className="glass-card" style={{ marginBottom: '2rem' }}>
                <h3 className="sport-font" style={{ fontSize: '1.2rem', marginBottom: '1rem' }}>Generar Reporte</h3>
                
                <div style={{ marginBottom: '1.5rem' }}>
                    <label style={{ display: 'block', fontSize: '0.8rem', color: 'var(--text-muted)' }}>Filtrar por Mes (Opcional)</label>
                    <input className="input-field" type="month" value={mes} onChange={(e) => setMes(e.target.value)} />
                    <small style={{ color: 'var(--text-muted)' }}>Si se deja en blanco asume toda la historia</small>
                </div>

                <button onClick={handleDownload} disabled={loading} className="btn-primary" style={{ width: '100%' }}>
                    {loading ? '⏳ Generando Excel...' : '📊 Descargar Excel'}
                </button>
            </div>
        </div>
    );
};

export default AdminLiquidaciones;
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(jsx)
    print("Updated AdminLiquidaciones.jsx")

def update_app_jsx():
    path = r"d:\Proyectos\Arbitros\frontend\src\App.jsx"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    if "AdminLiquidaciones" not in content:
        content = content.replace(
            "import AdminDesignaciones from './views/admin/AdminDesignaciones';",
            "import AdminDesignaciones from './views/admin/AdminDesignaciones';\nimport AdminLiquidaciones from './views/admin/AdminLiquidaciones';"
        )
        content = content.replace(
            "<Route path=\"/admin/designaciones\" element={<AdminDesignaciones />} />",
            "<Route path=\"/admin/designaciones\" element={<AdminDesignaciones />} />\n          <Route path=\"/admin/liquidaciones\" element={<AdminLiquidaciones />} />"
        )
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print("Updated App.jsx with Liquidaciones route")

if __name__ == "__main__":
    update_api_js()
    update_admin_liquidaciones_jsx()
    update_app_jsx()
    print("Build step for Admin Liquidaciones completed!")
