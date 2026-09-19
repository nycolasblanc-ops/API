import React from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

export const Home: React.FC = () => {
  const { logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div style={{ textAlign: 'center', marginTop: '50px' }}>
      <h1>¡Bienvenido a Nico - Shopping!</h1>
      <button onClick={handleLogout} style={{ padding: '10px 20px' }}>Cerrar Sesión</button>
    </div>
  );
};
