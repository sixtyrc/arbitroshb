import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/Layout';
import Login from './views/Login';
import Dashboard from './views/Dashboard';
import Disponibilidad from './views/Disponibilidad';
import Perfil from './views/Perfil';
import AdminDashboard from './views/admin/AdminDashboard';
import AdminPartidos from './views/admin/AdminPartidos';
import AdminDesignaciones from './views/admin/AdminDesignaciones';
import AdminLiquidaciones from './views/admin/AdminLiquidaciones';

function App() {
  const isAuthenticated = !!localStorage.getItem('access_token');
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Navigate to="/login" />} />
          <Route path="/login" element={<Login />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/disponibilidad" element={<Disponibilidad />} />
          <Route path="/perfil" element={<Perfil />} />
          
          {/* Vistas de Administrador */}
          <Route path="/admin" element={<AdminDashboard />} />
          <Route path="/admin/partidos" element={<AdminPartidos />} />
          <Route path="/admin/designaciones" element={<AdminDesignaciones />} />
          <Route path="/admin/liquidaciones" element={<AdminLiquidaciones />} />
          
          {/* Fallback */}
          <Route path="*" element={<Navigate to="/login" />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
