import { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [prefs, setPrefs] = useState({ time: 4.5, price: 100000, power: 'Petrol' });
  const [cars, setCars] = useState([]);

  const findCars = async () => {
    const res = await axios.post('http://localhost:5001/api/recommend', prefs);
    setCars(res.data);
  };

  return (
    <div className="main-container">
      <h1>🏎️ Sport Car Recommender</h1>
      <div className="form-box">
        <label>0-60 MPH: {prefs.time}s</label>
        <input type="range" min="2" max="10" step="0.1" onChange={e => setPrefs({...prefs, time: e.target.value})} />
        
        <label>Budget (USD): ${prefs.price}</label>
        <input type="number" value={prefs.price} onChange={e => setPrefs({...prefs, price: e.target.value})} />
        
        <button onClick={findCars}>Find My Car</button>
      </div>

      <div className="car-list">
        {cars.map((car, i) => (
          <div key={i} className="car-card">
            <h3>{car.name} {car.model}</h3>
            <p>${car.price.toLocaleString()} | {car.time}s</p>
          </div>
        ))}
      </div>
    </div>
  );
}
export default App;