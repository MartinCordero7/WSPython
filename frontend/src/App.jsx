import { useState, useEffect } from 'react';
import './App.css';

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:4010';

function App() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch(`${API_BASE}/api/items`)
      .then(response => {
        if (!response.ok) {
          throw new Error('Error al cargar los datos');
        }
        return response.json();
      })
      .then(data => {
        setItems(data);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  const formatDiscount = (value) => {
    if (value == null) return '';
    const pct = value > 1 ? value : value * 100;
    return `${pct.toFixed(0)}%`;
  };

  const formatTotalSale = (value) => {
    if (value == null) return '';
    return `$${value.toLocaleString('es-MX', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;  
  };

  if (loading) {
    return (
      <div className="container">
        <h1>Datos de MongoDB</h1>
        <p>Cargando...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container">
        <h1>Datos de MongoDB</h1>
        <p className="error">Error: {error}</p>
      </div>
    );
  }

  return (
    <div className="container">
      <div className="header">
        <h1>📋 Clientes MongoDB</h1>
      </div>

      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Nombre</th>
              <th>Email</th>
              <th>Tipo</th>
              <th>Descuento</th>
              <th>Total Venta</th>
            </tr>
          </thead>
          <tbody>
            {items.length === 0 ? (
              <tr>
                <td colSpan="6" className="no-data">
                  Sin datos
                </td>
              </tr>
            ) : (
              items.map((item, index) => (
                <tr key={item.id || index}>
                  <td>{item.id || ''}</td>
                  <td><strong>{item.fullName || ''}</strong></td>
                  <td>{item.email || ''}</td>
                  <td>{item.type || ''}</td>
                  <td className="num">{formatDiscount(item.discount)}</td>
                  <td className="num">{formatTotalSale(item.totalSale)}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default App;
