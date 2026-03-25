import sys        # <--- CRITICAL: Needed to read Node.js arguments
import json       # <--- CRITICAL: Needed to send data to the Frontend
import pandas as pd
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity

# --- DATA LOADING & CLEANING (Keep your existing code) ---
d = pd.read_csv("../ML_Engine/Sport car price.csv") # Path updated for Backend folder structure

# Standardize Price
d["Price (in USD)"] = d["Price (in USD)"].astype(str).str.replace('"', '').str.replace(',', '')
d["Price (in USD)"] = pd.to_numeric(d["Price (in USD)"], errors="coerce")

# Handle Powertrain
d["Powertrain"] = d["Engine Size (L)"].apply(lambda x: "Electric" if "electric" in str(x).lower() else "Petrol / Diesel")
d["0-60 MPH Time (seconds)"] = pd.to_numeric(d["0-60 MPH Time (seconds)"], errors="coerce")

# Drop nulls and duplicates
d.dropna(subset=["Price (in USD)", "0-60 MPH Time (seconds)"], inplace=True)
d = d.drop_duplicates().reset_index(drop=True)

# Prepare specific features for Similarity
d_n = d[["Car Name", "Car Model", "0-60 MPH Time (seconds)", "Price (in USD)", "Powertrain"]].copy()

# Feature Scaling for Cosine Similarity
features = ["0-60 MPH Time (seconds)", "Price (in USD)"]
scaler = MinMaxScaler()
d_scaled = scaler.fit_transform(d[features].fillna(0))
s = cosine_similarity(d_scaled)

# --- THE RECOMMENDATION LOGIC ---
def get_recommendations(Time, Price, Power):
    # Filter based on user preference
    c_n = d_n[
        (d_n["0-60 MPH Time (seconds)"].between(Time-2.0, Time+2.0)) & 
        (d_n["Price (in USD)"].between(Price*0.3, Price*1.7)) & 
        (d_n["Powertrain"].str.contains(Power, case=False, na=False))
    ].copy()
    
    if c_n.empty:
        return []

    # Find the "Anchor" car (closest to user input)
    c_n["total_diff"] = abs(c_n["0-60 MPH Time (seconds)"] - Time) + (abs(c_n["Price (in USD)"] - Price) / 100000)
    c_n = c_n.sort_values("total_diff").reset_index()
    
    anchor_idx = c_n.iloc[0]["index"]
    
    # Get top 5 similar cars using Cosine Similarity
    sim_scores = list(enumerate(s[anchor_idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    results = []
    seen_models = set()
    
    for i in sim_scores:
        idx = i[0]
        model = d_n.iloc[idx]["Car Model"]
        if model not in seen_models:
            results.append({
                "Car_Name": str(d_n.iloc[idx]["Car Name"]),
                "Car_Model": str(model),
                "Time": float(d_n.iloc[idx]["0-60 MPH Time (seconds)"]),
                "Price": float(d_n.iloc[idx]["Price (in USD)"])
            })
            seen_models.add(model)
        if len(results) >= 5:
            break
            
    return results

# --- THE BRIDGE (Main Execution) ---
if __name__ == "__main__":
    try:
        # Node.js sends: node server.js -> spawn('python', [script, time, price, power])
        arg_time = float(sys.argv[1])
        arg_price = float(sys.argv[2])
        arg_power = sys.argv[3]
        
        output = get_recommendations(arg_time, arg_price, arg_power)
        
        # Output ONLY the JSON string. Do not print anything else!
        print(json.dumps(output))
    except Exception as e:
        print(json.dumps([{"error": str(e)}]))