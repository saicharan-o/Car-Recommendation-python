import sys, json, pandas as pd, os

base_path = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(base_path, "Sport car price.csv")

def get_recommendations(u_time, u_price):
    if not os.path.exists(csv_path): return []
    
    df = pd.read_csv(csv_path)

    df["Price (in USD)"] = df["Price (in USD)"].astype(str).str.replace(r'[\$,"]', '', regex=True)
    df["Price (in USD)"] = pd.to_numeric(df["Price (in USD)"], errors="coerce")
    df["0-60 MPH Time (seconds)"] = pd.to_numeric(df["0-60 MPH Time (seconds)"], errors="coerce")
    df.dropna(subset=["Price (in USD)", "0-60 MPH Time (seconds)"], inplace=True)

    affordable = df[df["Price (in USD)"] <= u_price].copy()
    if affordable.empty: return []

    # 3. WEIGHTED SCORE:
    # We want cars CLOSEST to the budget (high budget = high price cars)
    # Price is 80% weight, Speed is 20% weight
    p_max = df["Price (in USD)"].max()
    t_max = df["0-60 MPH Time (seconds)"].max()

    # score: 0 is perfect. We find cars where (u_price - car_price) is small.
    affordable["score"] = (abs(affordable["Price (in USD)"] - u_price) / p_max * 0.8) + \
                          (abs(affordable["0-60 MPH Time (seconds)"] - u_time) / t_max * 0.2)

    # 4. REMOVE DUPLICATES (Fixes the Chevrolet repeating problem)
    # Sort by score first, then drop duplicates so we keep the best version
    affordable = affordable.sort_values("score")
    unique_cars = affordable.drop_duplicates(subset=["Car Name", "Car Model"])

    results = []
    for _, row in unique_cars.head(5).iterrows():
        results.append({
            "Car_Name": str(row["Car Name"]),
            "Car_Model": str(row["Car Model"]),
            "Time": float(row["0-60 MPH Time (seconds)"]),
            "Price": float(row["Price (in USD)"])
        })
    return results

if __name__ == "__main__":
    try:
        # Expects: [script.py, time, price]
        print(json.dumps(get_recommendations(float(sys.argv[1]), float(sys.argv[2]))))
    except:
        print(json.dumps([]))
        