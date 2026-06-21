import joblib
import pandas as pd

model = joblib.load(
    "models/impact_model.pkl"
)

event_encoder = joblib.load(
    "models/event_encoder.pkl"
)

risk_encoder = joblib.load(
    "models/risk_encoder.pkl"
)

event = event_encoder.transform(
    ["procession"]
)[0]

risk = risk_encoder.transform(
    ["Critical"]
)[0]

sample = pd.DataFrame([{

    "event_type": event,

    "crowd_size": 5000,

    "duration_hours": 4,

    "risk_level": risk

}])

prediction = model.predict(
    sample
)

print(
    "Predicted Impact:",
    round(prediction[0],2)
)