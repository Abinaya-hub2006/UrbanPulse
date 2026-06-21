import pandas as pd
import joblib

from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder


def retrain_model():

    df = pd.read_csv(
        "data/post_event_reviews.csv"
    )

    event_encoder = LabelEncoder()
    risk_encoder = LabelEncoder()

    df["event_type"] = event_encoder.fit_transform(
        df["event_type"]
    )

    df["risk_level"] = risk_encoder.fit_transform(
        df["risk_level"]
    )

    X = df[

        [
            "event_type",
            "crowd_size",
            "duration_hours",
            "risk_level"
        ]

    ]

    y = df["actual_impact"]

    model = RandomForestRegressor(
        n_estimators=200,
        random_state=42
    )

    model.fit(X, y)

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

    return len(df)