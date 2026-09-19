import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';

export const Login: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    try {
      // Reemplaza con la URL de tu API de C#
      const response = await axios.post('http://localhost:8080/auth/login', {
        email,
        password,
      });

      const { access_token } = response.data; // Tu API debe devolver { token: "..." }
      
      login(access_token);
      navigate('/home'); // Redirección automática
    } catch (err) {
      console.log(err);
      setError('Credenciales inválidas o error de conexión');
    }
  };

  return (
    <div style={{ maxWidth: '400px', margin: '50px auto', textAlign: 'center' }}>
      <h2>Biunvenido a Nico - Shopping</h2>
      <h3>Iniciar Sesión</h3>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <form onSubmit={handleSubmit}>
        <input 
          type="email" 
          placeholder="Email" 
          value={email} 
          onChange={(e) => setEmail(e.target.value)} 
          required 
          style={{ display: 'block', width: '100%', margin: '10px 0', padding: '8px' }}
        />
        <input 
          type="password" 
          placeholder="Contraseña" 
          value={password} 
          onChange={(e) => setPassword(e.target.value)} 
          required 
          style={{ display: 'block', width: '100%', margin: '10px 0', padding: '8px' }}
        />
        <button type="submit" style={{ width: '100%', padding: '10px' }}>Ingresar</button>
      </form>
    </div>
  );
};
