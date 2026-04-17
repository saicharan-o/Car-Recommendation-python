import sys        
import json       
import pandas as pd
import os                                  
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity

base_path = os.path.dirname(__file__)
csv_path = os.path.join(base_path, "Sport car price.csv")

d = pd.read_csv(csv_path)


d["Price (in USD)"] = d["Price (in USD)"].astype(str).str.replace('"', '').str.replace(',', '')
d["Price (in USD)"] = pd.to_numeric(d["Price (in USD)"], errors="coerce")

d["Powertrain"] = d["Engine Size (L)"].apply(lambda x: "Electric" if "electric" in str(x).lower() else "Petrol / Diesel")
d["0-60 MPH Time (seconds)"] = pd.to_numeric(d["0-60 MPH Time (seconds)"], errors="coerce")

d.dropna(subset=["Price (in USD)", "0-60 MPH Time (seconds)"], inplace=True)
d = d.drop_duplicates().reset_index(drop=True)

d_n = d[["Car Name", "Car Model", "0-60 MPH Time (seconds)", "Price (in USD)", "Powertrain"]].copy()

features = ["0-60 MPH Time (seconds)", "Price (in USD)"]
scaler = MinMaxScaler()
d_scaled = scaler.fit_transform(d[features].fillna(0))
s = cosine_similarity(d_scaled)

def get_recommendations(Time, Price, Power):

    c_n = d_n[d_n["Price (in USD)"] <= Price].copy()

    if c_n.empty:
        return []

    p_min, p_max = d_n["Price (in USD)"].min(), d_n["Price (in USD)"].max()
    t_min, t_max = d_n["0-60 MPH Time (seconds)"].min(), d_n["0-60 MPH Time (seconds)"].max()
    
    p_range = (p_max - p_min) if (p_max - p_min) > 0 else 1
    t_range = (t_max - t_min) if (t_max - t_min) > 0 else 1

    c_n["p_dist"] = abs(c_n["Price (in USD)"] - Price) / p_range
    c_n["t_dist"] = abs(c_n["0-60 MPH Time (seconds)"] - Time) / t_range
    
    c_n["total_diff"] = (c_n["p_dist"] * 0.7) + (c_n["t_dist"] * 0.3)

    final_matches = c_n.sort_values("total_diff").head(10)

    results = []
    seen_models = set()
    
    for _, row in final_matches.iterrows():
        model = row["Car Model"]
        if model not in seen_models:
            results.append({
                "Car_Name": str(row["Car Name"]),
                "Car_Model": str(model),
                "Time": float(row["0-60 MPH Time (seconds)"]),
                "Price": float(row["Price (in USD)"])
            })
            seen_models.add(model)
        if len(results) >= 5:
            break
            
    return results
            

if __name__ == "__main__":
    try:
        arg_time = float(sys.argv[1])
        arg_price = float(sys.argv[2])
        arg_power = sys.argv[3]
        
        output = get_recommendations(arg_time, arg_price, arg_power)
        
        print(json.dumps(output))
    except Exception as e:
        print(json.dumps([{"error": str(e)}]))
