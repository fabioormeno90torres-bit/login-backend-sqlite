import { useState } from 'react';

function App() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [mensaje, setMensaje] = useState('');
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const API_URL = "http://127.0.0.1:5000/api/login";

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
      });

      const data = await response.json();

      if (response.ok && data.success) {
        setIsLoggedIn(true);
        setMensaje(data.message);
      } else {
        setIsLoggedIn(false);
        setMensaje(data.message || "Error al iniciar sesión.");
      }
    } catch (error) {
      setMensaje("No se pudo conectar con el servidor Backend.");
    }
  };

  return (
    <div className="login-container">
      {!isLoggedIn ? (
        <form onSubmit={handleLogin}>
          <h2>Login (React + Flask + SQLite)</h2>
          
          <div className="form-group">
            <label>Usuario:</label>
            <input 
              type="text" 
              value={username} 
              onChange={(e) => setUsername(e.target.value)} 
              required 
            />
          </div>
          
          <div className="form-group">
            <label>Contraseña:</label>
            <input 
              type="password" 
              value={password} 
              onChange={(e) => setPassword(e.target.value)} 
              required 
            />
          </div>
          
          <button type="submit" className="btn-submit">Ingresar</button>
        </form>
      ) : (
        <div className="dashboard-container">
          <h2>Panel de Control</h2>
          <p className="success-message">{mensaje}</p>
          <button 
            onClick={() => { setIsLoggedIn(false); setUsername(''); setPassword(''); setMensaje(''); }} 
            className="btn-logout"
          >
            Cerrar Sesión
          </button>
        </div>
      )}

      {!isLoggedIn && mensaje && <p className="error-message">{mensaje}</p>}
    </div>
  );
}

export default App;