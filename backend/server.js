const path = require('path');
const express = require('express');
const { spawn } = require('child_process');
const cors = require('cors');
const app = express();

app.use(cors());
app.use(express.json());

app.post('/api/recommend', (req, res) => {
    const { time, price, power } = req.body;
    
    // FIX: The script is in the SAME 'Backend' folder as server.js
    const scriptPath = path.join(__dirname, 'CR-Backend.py'); 
    
    // Note: If 'python' doesn't work, try 'python3'
    const python = spawn('python', [scriptPath, time, price, power]);
    
    let output = "";
    let errorOutput = "";

    python.stdout.on('data', (data) => output += data.toString());
    python.stderr.on('data', (data) => errorOutput += data.toString());

    python.on('close', (code) => {
        if (code !== 0) {
            console.error("Python Error Output:", errorOutput);
            return res.json([]);
        }
        try {
            res.json(JSON.parse(output)); 
        } catch (e) { 
            console.error("JSON Parse Error. Raw Output:", output);
            res.json([]); 
        }
    });
});

app.listen(5001, () => console.log("Backend running on Port 5001"));