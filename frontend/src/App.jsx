import { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [prefs, setPrefs] = useState({ time: 4.7, price: 10000, power: 'Petrol' });
  const [cars, setCars] = useState([]);
  const [loading, setLoading] = useState(false);

  const findCars = async () => {
    setLoading(true);
    try {
      const res = await axios.post('http://localhost:5001/api/recommend', prefs);
      setCars(res.data);
    } catch (err) {
      alert("Error: Make sure your Backend is running!");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="main-container">
      <h1><span style={{color: '#e63946'}}>🏎️</span> Sport Car Recommender</h1>
      
      <div className="form-box">
        <div className="form-group">
          <label>0-60 MPH: {prefs.time}s</label>
          <input type="range" min="2" max="10" step="0.1" value={prefs.time}
            onChange={e => setPrefs({...prefs, time: e.target.value})} />
        </div>

        <div className="form-group">
          <label>Budget (USD)</label>
          <input type="number" value={prefs.price} 
            onChange={e => setPrefs({...prefs, price: e.target.value})} />
        </div>

        <button onClick={findCars}>{loading ? 'Searching...' : 'Find My Car'}</button>
      </div>

      <div className="car-grid">
        {cars.length > 0 ? cars.map((car, i) => (
          <div key={i} className="car-card">
            <h3>{car.name}</h3>
            <p style={{color: '#aaa', margin: '0'}}>Model: {car.model}</p>
            <p className="price-tag">${car.price?.toLocaleString()}</p>
            <p>⏱️ 0-60 MPH: {car.time}s</p>
          </div>
        )) : !loading && <p>Adjust sliders and click search to see results.</p>}
      </div>
    </div>
  );
}
export default App;