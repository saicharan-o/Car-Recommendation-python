import { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [prefs, setPrefs] = useState({ time: 3.5, price: 100000 });
  const [cars, setCars] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const findCars = async () => {
    setLoading(true);
    setCars([]);
    setError("");
    
    try {
      const res = await axios.post('http://localhost:5001/api/recommend', prefs);
      if (res.data && res.data.length > 0) {
        setCars(res.data);
      } else {
        setError("No cars found. Try increasing your budget!");
      }
    } catch (err) {
      setError("Server Error: Make sure the Backend is running.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="main-container">
      <h1>🏎️ Sport Car Recommender</h1>
      
      <div className="form-box">
        <div className="form-group">
          <label>Target 0-60 MPH: <strong>{prefs.time}s</strong></label>
          <input 
            type="range" min="1.8" max="7.0" step="0.1" 
            value={prefs.time}
            onChange={e => setPrefs({...prefs, time: Number(e.target.value)})} 
          />
        </div>

        <div className="form-group">
          <label>Max Budget (USD)</label>
          <input 
            type="number" value={prefs.price} 
            onChange={e => setPrefs({...prefs, price: Number(e.target.value)})} 
          />
        </div>
        <button onClick={findCars}>{loading ? 'CALCULATING...' : 'FIND MY CAR'}</button>
      </div>

      {error && <p className="error-text" style={{color: 'red'}}>{error}</p>}

      <div className="car-grid">
        {cars.map((car, i) => (
          <div key={i} className="car-card">
            <span className="time-tag">⏱️ {car.Time}s</span>
            <h3>{car.Car_Name}</h3>
            <p>Model: {car.Car_Model}</p>
            <p className="price-tag">${car.Price.toLocaleString()}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;