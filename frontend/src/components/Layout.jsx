import React from 'react';
import { useLocation, Link } from 'react-router-dom';

const Layout = ({ children }) => {
  const location = useLocation();
  
  // Checking auth superficially:
  const isAuthenticated = !!localStorage.getItem('access_token');
  
  // Hide nav on Login or Error pages
  const showNav = isAuthenticated && location.pathname !== '/login';

  return (
    <div className="app-container" style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh', paddingBottom: showNav ? '75px' : '0' }}>
      <main style={{ flex: 1 }}>
        {children}
      </main>
      
      {showNav ? (
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
      ) : (
        <footer className="app-footer">
          <p>© {new Date().getFullYear()} ArbitrosHB</p>
        </footer>
      )}
    </div>
  );
};

export default Layout;
