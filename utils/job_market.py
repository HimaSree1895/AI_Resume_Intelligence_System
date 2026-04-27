import pandas as pd
from sklearn.linear_model import LinearRegression

# Load dataset once
data = pd.read_csv("dataset/job_market.csv")

# Clean dataset values
data["Role"] = data["Role"].str.lower().str.strip()

def predict_job_demand(role):

    role = role.lower().strip()

    role_data = data[data["Role"] == role]

    # ✅ SAFETY CHECK
    if role_data.empty:
        return 1500   # default safe demand value

    X = role_data[["Year"]]
    y = role_data["Openings"]

    model = LinearRegression()
    model.fit(X, y)

    future_year = [[2025]]

    prediction = model.predict(future_year)[0]

    return int(prediction)
