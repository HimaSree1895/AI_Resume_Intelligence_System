import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import joblib

data = pd.read_csv(
"dataset/Placement_Data_Full_Class.csv"
)

data.drop(["sl_no","salary"],axis=1,inplace=True)

le = LabelEncoder()

for col in data.columns:
    if data[col].dtype=="object":
        data[col]=le.fit_transform(data[col])

X=data.drop("status",axis=1)
y=data["status"]

model=RandomForestClassifier()
model.fit(X,y)

joblib.dump(model,"model/placement_model.pkl")

print("Placement Model Ready")
