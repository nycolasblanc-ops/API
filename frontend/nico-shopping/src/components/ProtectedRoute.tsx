import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export const ProtectedRoute: React.FC = () => {
  const { isAuthenticated } = useAuth();

  // Si no está autenticado, redirige al login
  return isAuthenticated ? <Outlet /> : <Navigate to="/login" replace />;
};
