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
  
  try {
    const res = await axios.post('http://localhost:5001/api/recommend', prefs);
    if (res.data && res.data.length > 0) {
      setCars(res.data);
    } else {
      alert("No cars found matching your requirements in our dataset. Please try a different budget or speed range!");
    }
  } catch (err) {
    alert("Backend Error: Please check if server.js is running.");
  } finally {
    setLoading(false);
  }
};

  return (
    <div className="main-container">
    {/* CUSTOM ERROR TOAST */}
    {error && <div className="error-toast">{error}</div>}
      <h1>🏎️ Sport Car Recommender</h1>
      
      <div className="form-box">
        {/* --- REPLACED START --- */}
       <div className="form-group">
  <label>Target 0-60 MPH: <strong>{prefs.time}s</strong></label>
  <input 
    type="range" 
    min="1.8"   // Least value in CSV (Rimac)
    max="7.0"   // High end for sport cars in CSV
    step="0.1" 
    value={prefs.time}
    onChange={e => setPrefs({...prefs, time: Number(e.target.value)})} 
  />
</div>

       <div className="form-group">
  <label>Max Budget (USD)</label>
  <input 
    type="number" 
    min="30000"     // Least price in CSV (approx)
    max="4000000"   // Highest price (Bugatti is 3.9M)
    value={prefs.price} 
    placeholder="e.g. 500000"
    onChange={e => {
        let val = Number(e.target.value);
        // If user tries to go above the highest car in data, cap it at 4M
        if(val > 4000000) val = 4000000; 
        setPrefs({...prefs, price: val});
    }} 
  />
</div>
        {/* --- REPLACED END --- */}

        <button onClick={findCars}>{loading ? 'CALCULATING...' : 'FIND MY CAR'}</button>
      </div>

      <div className="car-grid">
        {cars.map((car, i) => (
          <div key={i} className="car-card">
            <span className="time-tag">⏱️ {car.Time} Seconds</span>
            <h3>{car.Car_Name}</h3>
            <p style={{color: '#888'}}>Model: {car.Car_Model}</p>
            <p className="price-tag">${car.Price?.toLocaleString() ? car.Price.toLocaleString() : car.Price}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
