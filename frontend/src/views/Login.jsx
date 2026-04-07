import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { authService } from '../services/api';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    try {
      await authService.login(username, password);
      navigate('/dashboard');
    } catch (err) {
      setError('Credenciales inválidas. Reintentá.');
    }
  };

  return (
    <div className="container" style={{ display: 'flex', alignItems: 'center', minHeight: '80vh' }}>
      <div className="glass-card" style={{ width: '100%' }}>
        <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
          <h1 className="sport-font" style={{ fontSize: '2.5rem', color: 'var(--secondary)' }}>
            Arbitros<span style={{ color: 'var(--text)' }}>HB</span>
          </h1>
          <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
            Colegio de Árbitros - Chaco
          </p>
        </div>

        <form onSubmit={handleLogin}>
          {error && (
            <div style={{ color: 'var(--error)', fontSize: '0.8rem', marginBottom: '1rem', textAlign: 'center' }}>
              {error}
            </div>
          )}
          <div className="input-group">
            <label>Usuario</label>
            <input 
              type="text" 
              placeholder="Ej: nahuel_ref" 
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>

          <div className="input-group">
            <label>Contraseña</label>
            <input 
              type="password" 
              placeholder="••••••••" 
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          <button type="submit" className="btn-primary">
            Entrar a la Cancha
          </button>
        </form>

        <div style={{ marginTop: '1.5rem', textAlign: 'center', fontSize: '0.8rem' }}>
          <a href="#" style={{ color: 'var(--text-muted)', textDecoration: 'none' }}>
            ¿Olvidaste tu acceso? Contactar Admin
          </a>
        </div>
      </div>
    </div>
  );
};

export default Login;
