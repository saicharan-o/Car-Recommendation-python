const express = require('express');
const { spawn } = require('child_process');
const cors = require('cors');
const app = express();

app.use(cors());
app.use(express.json());

app.post('/api/recommend', (req, res) => {
    const { time, price, power } = req.body;
    const python = spawn('python', ['../ML_Engine/CR-Backend.py', time, price, power]);

    let output = "";
    python.stdout.on('data', (data) => output += data.toString());
    python.on('close', () => {
        try { res.json(json.parse(output)); } 
        catch (e) { res.json([]); }
    });
});

app.listen(5001, () => console.log("Backend running on Port 5001"));