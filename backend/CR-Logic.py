import sys        
import json       
import pandas as pd
import os                                          

# Get the absolute path to ensure Node.js can find the CSV
base_path = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(base_path, "Sport car price.csv")

def get_recommendations(user_time, user_price, power):
    if not os.path.exists(csv_path):
        return [{"error": "CSV file not found"}]

    df = pd.read_csv(csv_path)

    # 1. Clean Data (Removing commas and dollar signs)
    df["Price (in USD)"] = df["Price (in USD)"].astype(str).str.replace(r'[\$,"]', '', regex=True).str.strip()
    df["Price (in USD)"] = pd.to_numeric(df["Price (in USD)"], errors="coerce")
    df["0-60 MPH Time (seconds)"] = pd.to_numeric(df["0-60 MPH Time (seconds)"], errors="coerce")
    df.dropna(subset=["Price (in USD)", "0-60 MPH Time (seconds)"], inplace=True)

    # 2. Soft Filtering Logic
    # We find cars that are as close as possible to the budget
    # instead of just doing a "less than" filter which returns nothing.
    
    # Calculate a 'Match Score' (Lower is better)
    # We normalize the price and time so one doesn't dominate the other
    price_max = df["Price (in USD)"].max()
    time_max = df["0-60 MPH Time (seconds)"].max()

    df["score"] = (abs(df["Price (in USD)"] - user_price) / price_max) + \
                  (abs(df["0-60 MPH Time (seconds)"] - user_time) / time_max)

    # Sort by the best match score
    recommendations = df.sort_values("score").head(5)

    results = []
    for _, row in recommendations.iterrows():
        results.append({
            "Car_Name": str(row["Car Name"]),
            "Car_Model": str(row["Car Model"]),
            "Time": float(row["0-60 MPH Time (seconds)"]),
            "Price": float(row["Price (in USD)"])
        })
            
    return results

if __name__ == "__main__":
    try:
        # Node.js sends arguments as strings; we convert them here
        t = float(sys.argv[1]) if len(sys.argv) > 1 else 3.5
        p = float(sys.argv[2]) if len(sys.argv) > 2 else 100000
        pw = sys.argv[3] if len(sys.argv) > 3 else "Petrol"
        
        print(json.dumps(get_recommendations(t, p, pw)))
    except Exception as e:
        print(json.dumps([{"error": str(e)}]))