import React from 'react';

const Layout = ({ children }) => {
  return (
    <div className="app-container" style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <main style={{ flex: 1 }}>
        {children}
      </main>
      
      <footer className="app-footer">
        <p>© {new Date().getFullYear()} Todos los derechos reservados</p>
        <p>
          Desarrollado por <a href="https://ctsoft.com.ar" target="_blank" rel="noopener noreferrer">CTSoft</a>
        </p>
      </footer>
    </div>
  );
};

export default Layout;
