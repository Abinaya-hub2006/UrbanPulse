import joblib
import pandas as pd

# =====================================
# LOAD TRAINED MODEL
# =====================================

model = joblib.load(
    "models/impact_model.pkl"
)

event_encoder = joblib.load(
    "models/event_encoder.pkl"
)

risk_encoder = joblib.load(
    "models/risk_encoder.pkl"
)


def simulate_event(
    event_cause,
    priority,
    road_closure,
    risk_level,
    duration_hours,
    crowd_size
):

    # Encode values

    try:

        event_encoded = event_encoder.transform(
            [event_cause]
        )[0]

    except:

        event_encoded = 0

    try:

        risk_encoded = risk_encoder.transform(
            [risk_level]
        )[0]

    except:

        risk_encoded = 0

    # Prediction Input

    sample = pd.DataFrame([{

        "event_type":
            event_encoded,

        "crowd_size":
            crowd_size,

        "duration_hours":
            duration_hours,

        "risk_level":
            risk_encoded

    }])

    # ML Prediction

    impact_score = float(
        model.predict(sample)[0]
    )

    # Resource Recommendation

    officers_mid = min(
        impact_score * 1.5,
        40
    )

    barricades_mid = min(
        impact_score * 2.5,
        70
    )

    officers_min = round(
        officers_mid * 0.8
    )

    officers_max = round(
        officers_mid * 1.2
    )

    barricades_min = round(
        barricades_mid * 0.8
    )

    barricades_max = round(
        barricades_mid * 1.2
    )

    # Response

    if impact_score < 8:

        response = "Routine"

    elif impact_score < 15:

        response = "Urgent"

    else:

        response = "Critical"

    return {

        "response":
            response,

        "impact_score":
            round(
                impact_score,
                2
            ),

        "officers_range":
            f"{officers_min}-{officers_max}",

        "barricades_range":
            f"{barricades_min}-{barricades_max}"

    }


# =====================================
# Duration Analysis
# =====================================

def duration_sensitivity_analysis(
    event_cause,
    priority,
    road_closure,
    risk_level,
    crowd_size
):

    results = []

    for duration in [1,2,4,6,8]:

        result = simulate_event(

            event_cause,

            priority,

            road_closure,

            risk_level,

            duration,

            crowd_size

        )

        results.append({

            "duration_hours":
                duration,

            "impact_score":
                result["impact_score"]

        })

    return results


# =====================================
# Crowd Analysis
# =====================================

def crowd_sensitivity_analysis(
    event_cause,
    priority,
    road_closure,
    risk_level,
    duration_hours
):

    results = []

    for crowd in [

        100,
        500,
        1000,
        3000,
        5000,
        10000

    ]:

        result = simulate_event(

            event_cause,

            priority,

            road_closure,

            risk_level,

            duration_hours,

            crowd

        )

        results.append({

            "crowd_size":
                crowd,

            "impact_score":
                result["impact_score"]

        })

    return results


if __name__ == "__main__":

    print(

        simulate_event(

            "procession",

            "High",

            True,

            "Critical",

            4,

            5000

        )

    )