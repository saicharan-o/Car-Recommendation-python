import sys        
import json       
import pandas as pd
import os                                          

# FIX: Get the absolute path to the CSV in the same folder
base_path = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(base_path, "Sport car price.csv")

def get_recommendations(Time, Price, Power):
    if not os.path.exists(csv_path):
        return []

    d = pd.read_csv(csv_path)

    # Data Cleaning
    d["Price (in USD)"] = d["Price (in USD)"].astype(str).str.replace('"', '').str.replace(',', '').str.replace('$', '').str.strip()
    d["Price (in USD)"] = pd.to_numeric(d["Price (in USD)"], errors="coerce")
    d["0-60 MPH Time (seconds)"] = pd.to_numeric(d["0-60 MPH Time (seconds)"], errors="coerce")
    d.dropna(subset=["Price (in USD)", "0-60 MPH Time (seconds)"], inplace=True)

    # 1. SOFT FILTER: Try filtering by budget. 
    # If no cars exist under budget, use the whole dataset to find the "closest"
    c_n = d[d["Price (in USD)"] <= Price].copy()
    if c_n.empty:
        c_n = d.copy()

    # 2. Proximity Calculation
    p_min, p_max = d["Price (in USD)"].min(), d["Price (in USD)"].max()
    t_min, t_max = d["0-60 MPH Time (seconds)"].min(), d["0-60 MPH Time (seconds)"].max()
    
    p_range = (p_max - p_min) if (p_max - p_min) > 0 else 1
    t_range = (t_max - t_min) if (t_max - t_min) > 0 else 1

    # Calculate difference score (Lower is better)
    c_n["p_dist"] = abs(c_n["Price (in USD)"] - Price) / p_range
    c_n["t_dist"] = abs(c_n["0-60 MPH Time (seconds)"] - Time) / t_range
    c_n["total_diff"] = (c_n["p_dist"] * 0.7) + (c_n["t_dist"] * 0.3)

    final_matches = c_n.sort_values("total_diff").head(10)

    results = []
    seen_models = set()
    for _, row in final_matches.iterrows():
        model = str(row["Car Model"])
        if model not in seen_models:
            results.append({
                "Car_Name": str(row["Car Name"]),
                "Car_Model": model,
                "Time": float(row["0-60 MPH Time (seconds)"]),
                "Price": float(row["Price (in USD)"])
            })
            seen_models.add(model)
        if len(results) >= 5:
            break
            
    return results

if __name__ == "__main__":
    try:
        arg_time = float(sys.argv[1]) if len(sys.argv) > 1 else 3.5
        arg_price = float(sys.argv[2]) if len(sys.argv) > 2 else 100000
        arg_power = sys.argv[3] if len(sys.argv) > 3 else "Petrol"
        
        print(json.dumps(get_recommendations(arg_time, arg_price, arg_power)))
    except Exception as e:
        print(json.dumps([]))