const express = require('express');
const { spawn } = require('child_process');
const cors = require('cors');
const app = express();

app.use(cors());
app.use(express.json());

app.post('/api/recommend', (req, res) => {
    const { time, price, power } = req.body;
    // Ensure the path is correct relative to the backend folder
    const python = spawn('python', ['../ML_Engine/CR-Backend.py', time, price, power]);

    let output = "";
    python.stdout.on('data', (data) => output += data.toString());
    python.on('close', () => {
        try { 
            // FIX: JSON must be capitalized!
            res.json(JSON.parse(output)); 
        } 
        catch (e) { 
            console.error("Python Output Error:", output);
            res.json([]); 
        }
    });
});

app.listen(5001, () => console.log("Backend running on Port 5001"));