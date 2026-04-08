import os

def fix_footer():
    path = r"d:\Proyectos\Arbitros\frontend\src\components\Layout.jsx"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    new_jsx = """import React from 'react';
import { useLocation, Link } from 'react-router-dom';

const Layout = ({ children }) => {
  const location = useLocation();
  
  // Checking auth superficially:
  const isAuthenticated = !!localStorage.getItem('access_token');
  
  // Hide nav on Login or Error pages
  const showNav = isAuthenticated && location.pathname !== '/login';

  return (
    <div className="app-container" style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh', paddingBottom: showNav ? '75px' : '0' }}>
      <main style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
        <div style={{ flex: 1 }}>
            {children}
        </div>
        
        {/* Footer Discreto - Siempre Presente al final del contenido */}
        <footer className="app-footer" style={{ padding: '1.5rem', textAlign: 'center', opacity: 0.7 }}>
          <p style={{ margin: 0, fontSize: '0.75rem', color: 'var(--text-muted)' }}>
            © {new Date().getFullYear()} ArbitrosHB. Todos los derechos reservados.
          </p>
          <p style={{ margin: '5px 0 0 0', fontSize: '0.75rem', color: 'var(--text-muted)' }}>
            Desarrollado por <a href="https://ctsoft.com.ar" target="_blank" rel="noopener noreferrer" style={{ color: 'var(--primary)', textDecoration: 'none', fontWeight: 600 }}>CTSoft</a>
          </p>
        </footer>
      </main>
      
      {showNav && (
        <nav className="bottom-nav">
          <Link to="/dashboard" className={`nav-item ${location.pathname.startsWith('/dashboard') ? 'active' : ''}`}>
            <span className="nav-icon">🏠</span>
            <span>Inicio</span>
          </Link>
          <Link to="/disponibilidad" className={`nav-item ${location.pathname.startsWith('/disponibilidad') ? 'active' : ''}`}>
            <span className="nav-icon">📅</span>
            <span>Agenda</span>
          </Link>
          <Link to="/perfil" className={`nav-item ${location.pathname.startsWith('/perfil') ? 'active' : ''}`}>
            <span className="nav-icon">👤</span>
            <span>Perfil</span>
          </Link>
        </nav>
      )}
    </div>
  );
};

export default Layout;
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_jsx)
    print("Updated Layout.jsx with persistent global styling footer")

if __name__ == "__main__":
    fix_footer()
