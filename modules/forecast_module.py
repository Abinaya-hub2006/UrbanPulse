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


def predict_impact(
    event_type,
    crowd_size,
    duration_hours,
    risk_level
):

    event_encoded = event_encoder.transform(
        [event_type]
    )[0]

    risk_encoded = risk_encoder.transform(
        [risk_level]
    )[0]

    sample = pd.DataFrame([{

        "event_type": event_encoded,

        "crowd_size": crowd_size,

        "duration_hours": duration_hours,

        "risk_level": risk_encoded

    }])

    prediction = model.predict(
        sample
    )[0]

    return round(
        float(prediction),
        2
    )