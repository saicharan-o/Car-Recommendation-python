
import pandas as pd
from sklearn.preprocessing import LabelEncoder
d=pd.read_csv("Sport car price.csv")
d["Price (in USD)"]=d["Price (in USD)"].apply(lambda x:[i.replace('""','') for i in x])
d["Price (in USD)"]=d["Price (in USD)"].apply(lambda x:[i.replace(',','') for i in x])
d["Price (in USD)"]=d["Price (in USD)"].apply(lambda x:"".join(x))

d["Powertrain"] = d["Engine Size (L)"].apply(lambda x: "Electric" if "electric" in str(x).lower() else "Petrol / Diesel")
d["Engine Size (L)"] = (d["Engine Size (L)"].astype(str).str.replace('"', '', regex=False).str.replace(',', '', regex=False))
d["Engine Size (L)"] = pd.to_numeric(d["Engine Size (L)"], errors="coerce")
d.loc[d["Powertrain"] == "Electric", "Engine Size (L)"] = 0

d["Horsepower"]=d["Horsepower"].apply(lambda x:[i.replace('""','') for i in x])
d["Horsepower"]=d["Horsepower"].apply(lambda x:[i.replace(',','') for i in x])
d["Horsepower"]=d["Horsepower"].apply(lambda x:"".join(x))

d["Torque (lb-ft)"]=d["Torque (lb-ft)"].apply(lambda x: str(x).replace('""','').replace(',',''))
d["0-60 MPH Time (seconds)"] = pd.to_numeric(d["0-60 MPH Time (seconds)"], errors="coerce")
d["Price (in USD)"] = pd.to_numeric(d["Price (in USD)"], errors="coerce")
print(d.head())
print(d.info())
d.dropna(inplace=True)
print(d.isnull().sum())
d=d.drop_duplicates()
d=d.reset_index(drop=True)
print(d.duplicated().sum())
a=d
a.to_csv("Car Price.csv",index=False)
print(d.shape)
d_n=d[["Car Name","Car Model","0-60 MPH Time (seconds)","Price (in USD)","Powertrain"]]
print(d_n.head(10))
d_e=d_n.copy()
c=LabelEncoder()
d_e["Car Name"]=c.fit_transform(d_e["Car Name"])
d_e["Powertrain"]=c.fit_transform(d_e["Powertrain"])
d_e["Car Model"]=c.fit_transform(d_e["Car Model"])
print(d_e.head())
from sklearn.preprocessing import MinMaxScaler
features = ["0-60 MPH Time (seconds)", "Price (in USD)", "Horsepower", "Torque (lb-ft)"]
for col in features:
    d[col] = pd.to_numeric(d[col], errors='coerce')
scaler = MinMaxScaler()
d_e = scaler.fit_transform(d[features].fillna(0))
print("DATE:",d_e)
from sklearn.metrics.pairwise import cosine_similarity
s=cosine_similarity(d_e)

def recommad(Time,Price,Power):
    d_n.loc[:,"0-60 MPH Time (seconds)"] = d_n["0-60 MPH Time (seconds)"].astype(float)
    d_n.loc[:,"Price (in USD)"] = d_n["Price (in USD)"].astype(float)
    c_n=d_n[(d_n["0-60 MPH Time (seconds)"].between(Time-1.5,Time+1.5)) & (d_n["Price (in USD)"].between(Price*0.5,Price*1.5)) & (d_n["Powertrain"].str.contains(Power,case=False,na=False))].copy()
    if c_n.empty:
        print("Car Not found enter another data")
        return None
    c_n["time_diff"] = abs(c_n["0-60 MPH Time (seconds)"] - Time)
    c_n["price_diff"] = abs(c_n["Price (in USD)"] - Price)
    c_n["total_diff"] = c_n["time_diff"] + (c_n["price_diff"] / 100000) 
    c_n = c_n.sort_values("total_diff").reset_index()    
    c_f=c_n.iloc[0]["index"]
    s_c_n = d_n.loc[c_f, "Car Name"]
    s_c_m = d_n.loc[c_f, "Car Model"]
    print(f"Based on your input, the closest match is: \nCar Name: {s_c_n}\nCar Model: {s_c_m}\n0-60 MPH Time (seconds): {d_n.loc[c_f,"0-60 MPH Time (seconds)"]}\nPrice (in USD): {d_n.loc[c_f,"Price (in USD)"]}")
    c_l=list(enumerate(s[c_f]))
    # print(c_l)
    c_l=sorted(c_l,reverse=True,key=lambda x:x[1])
    rd=[]
    s_m=set()
    s_m.add(s_c_m)
    for i in c_l:
        idx=i[0]
        score=i[1]
        c_m=d_n.iloc[idx]["Car Model"]
        c_n=d_n.iloc[idx]["Car Name"]

        if c_m in s_m:
            continue
        rd.append(idx)
        s_m.add(c_m)

        if len(rd)>=5:
            break
    print("\nRecommended: ")    
    for idx in rd:
        print(f"\n Car Name:  {d_n.loc[idx,'Car Name']}\n Car Model:  {d_n.loc[idx,'Car Model']}\n 0-60 MPH Time (seconds): {d_n.loc[idx,'0-60 MPH Time (seconds)']}\n Price (in USD): {d_n.loc[idx,'Price (in USD)']}")
        print(f"Similarity Score: {score:.4f}")
recommad(Time=6.5,Price=50000,Power='petrol')