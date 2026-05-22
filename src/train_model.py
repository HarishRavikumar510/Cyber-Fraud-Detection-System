import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# LOAD DATASET
df = pd.read_csv("data/fraud_dataset.csv")

# CONVERT TEXT VALUES TO NUMBERS
df["transaction_type"] = df["transaction_type"].map({
    "UPI": 0,
    "Credit Card": 1,
    "Bank Transfer": 2
})

# FEATURES
X = df[["amount", "transaction_type", "device_risk"]]

# LABEL
y = df["is_fraud"]

# SPLIT DATA
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# CREATE MODEL
model = RandomForestClassifier()

# TRAIN MODEL
model.fit(X_train, y_train)

# SAVE MODEL
joblib.dump(model, "models/fraud_model.pkl")

print("✅ Model Trained Successfully")