import os

def update_index_css():
    path = r"d:\Proyectos\Arbitros\frontend\src\index.css"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    new_css = """
/* ---- Bottom Navigation (Tab Bar) ---- */
.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 65px;
  background: var(--glass);
  backdrop-filter: blur(12px);
  border-top: 1px solid var(--border);
  display: flex;
  justify-content: space-around;
  align-items: center;
  z-index: 1000;
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: var(--text-muted);
  text-decoration: none;
  font-family: 'Inter', sans-serif;
  font-size: 0.7rem;
  font-weight: 600;
  transition: var(--transition);
  padding: 0.5rem;
}

.nav-item .nav-icon {
  font-size: 1.5rem;
  margin-bottom: 2px;
}

.nav-item.active {
  color: var(--primary);
}

.nav-item.active .nav-icon {
  transform: scale(1.1);
}
"""

    if ".bottom-nav" not in content:
        # Append to the end of the file
        with open(path, "a", encoding="utf-8") as f:
            f.write(new_css)
        print("Updated index.css with .bottom-nav")

def update_layout_jsx():
    path = r"d:\Proyectos\Arbitros\frontend\src\components\Layout.jsx"
    jsx = """import React from 'react';
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
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(jsx)
    print("Updated Layout.jsx with Tab Bar")

def update_perfil_jsx():
    path = r"d:\Proyectos\Arbitros\frontend\src\views\Perfil.jsx"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Append the Admin Access button if the user is an admin.
    if "Panel Administrador" not in content:
        admin_btn = """
                {/* Boton secreto si es ADMIN */}
                {perfil?.user_data?.role === 'ADMIN' && (
                    <div style={{ marginTop: '2rem' }}>
                        <button 
                            className="btn-primary" 
                            style={{ background: 'var(--accent)' }} 
                            onClick={() => window.location.href='/admin'}
                        >
                            👑 Ingresar al Panel Administrador
                        </button>
                    </div>
                )}
"""
        # Let's insert it before the closing </div> of the main container, or simple append it
        # Try to find the section related to CBU/Alias
        content = content.replace(
            "</form>\n            </div>\n        </div>",
            f"</form>\n            </div>\n{admin_btn}\n        </div>"
        )
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print("Updated Perfil.jsx with Admin button")


if __name__ == "__main__":
    update_index_css()
    update_layout_jsx()
    update_perfil_jsx()
    print("Build step for Mobile Nav completed!")
