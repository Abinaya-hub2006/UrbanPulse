import pandas as pd
import joblib

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score
from sklearn.preprocessing import LabelEncoder

# =====================================
# LOAD DATA
# =====================================

df = pd.read_csv(
    "data/training_data.csv"
)

print("Dataset Shape:", df.shape)

# =====================================
# ENCODING
# =====================================

event_encoder = LabelEncoder()
risk_encoder = LabelEncoder()

df["event_type"] = event_encoder.fit_transform(
    df["event_type"]
)

df["risk_level"] = risk_encoder.fit_transform(
    df["risk_level"]
)

# =====================================
# FEATURES
# =====================================

X = df[

    [
        "event_type",
        "crowd_size",
        "duration_hours",
        "risk_level"
    ]

]

y = df["impact_score"]

# =====================================
# TRAIN TEST SPLIT
# =====================================

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.2,

    random_state=42

)

# =====================================
# MODEL
# =====================================

model = RandomForestRegressor(

    n_estimators=300,

    max_depth=12,

    random_state=42,

    n_jobs=-1

)

model.fit(

    X_train,
    y_train

)

# =====================================
# EVALUATION
# =====================================

preds = model.predict(
    X_test
)

mae = mean_absolute_error(
    y_test,
    preds
)

r2 = r2_score(
    y_test,
    preds
)

print("\nModel Performance")

print("MAE :", round(mae, 3))
print("R2  :", round(r2, 3))

# =====================================
# SAVE MODEL
# =====================================

joblib.dump(
    model,
    "models/impact_model.pkl"
)

joblib.dump(
    event_encoder,
    "models/event_encoder.pkl"
)

joblib.dump(
    risk_encoder,
    "models/risk_encoder.pkl"
)

print("\nSaved Successfully")

print("impact_model.pkl")
print("event_encoder.pkl")
print("risk_encoder.pkl")