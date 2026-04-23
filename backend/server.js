const path = require('path'); // Add this at the top
const express = require('express');
const { spawn } = require('child_process');
const cors = require('cors');
const app = express();

app.use(cors());

app.use(express.json());

app.post('/api/recommend', (req, res) => {

    const { time, price, power } = req.body;
    const scriptPath = path.join(__dirname, '..', 'ML_Engine', 'CR-Backend.py');
    const python = spawn('python', [scriptPath, time, price, power]);
    let output = "";
    python.stdout.on('data', (data) => output += data.toString());
    python.on('close', () => {

        try {
            res.json(JSON.parse(output)); 
        } 
        catch (e) { 
            console.error("Python Output Error:", output);
            res.json([]); 
        }
        
    });
});


// server.js
app.listen(5001, () => console.log("Backend running on Port 5001"));
