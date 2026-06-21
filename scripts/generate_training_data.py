import pandas as pd
import numpy as np

# =====================================
# LOAD DATA
# =====================================

df = pd.read_csv(
    "data/Astram_event_data.csv"
)

print("Rows:", len(df))

# =====================================
# CLEAN
# =====================================

df = df.copy()

df["event_cause"] = (
    df["event_cause"]
    .fillna("others")
    .astype(str)
)

df["priority"] = (
    df["priority"]
    .fillna("Low")
    .astype(str)
)

# =====================================
# EVENT SEVERITY
# =====================================

severity_map = {

    "vehicle_breakdown": 1,
    "pot_holes": 1,
    "debris": 1,

    "construction": 2,
    "water_logging": 2,
    "road_conditions": 2,
    "tree_fall": 2,

    "accident": 3,
    "congestion": 3,

    "public_event": 4,
    "procession": 4,

    "vip_movement": 5,
    "protest": 5

}

df["event_severity"] = (

    df["event_cause"]

    .str.lower()

    .map(severity_map)

    .fillna(2)

)

# =====================================
# SYNTHETIC CROWD SIZE
# =====================================

crowd_map = {

    "vehicle_breakdown": 100,
    "pot_holes": 100,
    "debris": 150,

    "construction": 500,
    "water_logging": 700,

    "accident": 800,
    "congestion": 1200,

    "public_event": 5000,
    "procession": 7000,

    "vip_movement": 3000,
    "protest": 8000

}

df["crowd_size"] = (

    df["event_cause"]

    .str.lower()

    .map(crowd_map)

    .fillna(1000)

)

# add randomness

df["crowd_size"] = (

    df["crowd_size"]

    *

    np.random.uniform(
        0.7,
        1.3,
        len(df)
    )

).astype(int)

# =====================================
# SYNTHETIC DURATION
# =====================================

duration_map = {

    "vehicle_breakdown": 1,
    "pot_holes": 1,

    "construction": 6,
    "water_logging": 4,

    "accident": 2,

    "public_event": 5,
    "procession": 6,

    "vip_movement": 3,
    "protest": 7

}

df["duration_hours"] = (

    df["event_cause"]

    .str.lower()

    .map(duration_map)

    .fillna(2)

)

# add randomness

df["duration_hours"] = (

    df["duration_hours"]

    *

    np.random.uniform(
        0.8,
        1.2,
        len(df)
    )

)

# =====================================
# RISK LEVEL
# =====================================

risk_score = (

    df["event_severity"]

    +

    np.where(
        df["priority"]
        .str.lower()
        ==
        "high",
        2,
        0
    )

    +

    np.where(
        df["requires_road_closure"]
        ==
        True,
        2,
        0
    )

)

risk_level = []

for score in risk_score:

    if score <= 3:
        risk_level.append("Low")

    elif score <= 5:
        risk_level.append("Medium")

    elif score <= 7:
        risk_level.append("High")

    else:
        risk_level.append("Critical")

df["risk_level"] = risk_level

# =====================================
# IMPACT SCORE (TARGET)
# =====================================

impact_score = (

    df["event_severity"] * 2

    +

    np.where(
        df["priority"]
        .str.lower()
        ==
        "high",
        4,
        0
    )

    +

    np.where(
        df["requires_road_closure"]
        ==
        True,
        5,
        0
    )

    +

    (df["crowd_size"] / 1000)

    +

    df["duration_hours"]

)

df["impact_score"] = (

    impact_score

    .round(2)

)

# =====================================
# FINAL TRAINING DATA
# =====================================

training_df = df[

    [

        "event_cause",

        "crowd_size",

        "duration_hours",

        "risk_level",

        "impact_score"

    ]

].copy()

training_df.columns = [

    "event_type",

    "crowd_size",

    "duration_hours",

    "risk_level",

    "impact_score"

]

# =====================================
# SAVE
# =====================================

training_df.to_csv(

    "data/training_data.csv",

    index=False

)

print(
    "Saved:",
    training_df.shape
)

print(
    training_df.head()
)