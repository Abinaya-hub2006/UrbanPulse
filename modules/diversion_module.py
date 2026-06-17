"""
Diversion Planning Engine

Module 4

Purpose:
- Find alternative low-risk junctions
- Calculate nearest diversion points
- Generate diversion recommendations
- Create diversion maps

Used by:
- Diversion Planner Page
"""

import pandas as pd
import folium

from math import radians
from math import sin
from math import cos
from math import sqrt
from math import atan2


# -----------------------------------
# Load Data
# -----------------------------------

def load_junction_data():

    return pd.read_csv(
        "data/junction_risk_table.csv"
    )


# -----------------------------------
# Haversine Distance
# -----------------------------------

def haversine(

    lat1,
    lon1,
    lat2,
    lon2

):

    R = 6371

    dlat = radians(
        lat2 - lat1
    )

    dlon = radians(
        lon2 - lon1
    )

    a = (

        sin(dlat / 2) ** 2

        +

        cos(radians(lat1))

        *

        cos(radians(lat2))

        *

        sin(dlon / 2) ** 2

    )

    c = 2 * atan2(
        sqrt(a),
        sqrt(1 - a)
    )

    return R * c


# -----------------------------------
# Diversion Recommendation
# -----------------------------------

def suggest_diversion(

    junction_data,
    affected_junction,
    top_n=3

):

    source = junction_data[

        junction_data["junction"]

        == affected_junction

    ]

    if len(source) == 0:

        return pd.DataFrame()

    lat = source.iloc[0]["latitude"]

    lon = source.iloc[0]["longitude"]

    candidates = junction_data[

        junction_data["risk_level"]

        .isin(

            ["Low", "Medium"]

        )

    ].copy()

    candidates = candidates[

        candidates["junction"]

        != affected_junction

    ]

    candidates["distance"] = (

        candidates.apply(

            lambda row:

            haversine(

                lat,
                lon,

                row["latitude"],
                row["longitude"]

            ),

            axis=1

        )

    )

    candidates = (

        candidates

        .sort_values(
            "distance"
        )

        .head(top_n)

    )

    return candidates[
        [

            "junction",

            "latitude",

            "longitude",

            "risk_level",

            "distance"

        ]
    ]


# -----------------------------------
# Diversion Map
# -----------------------------------

def create_diversion_map(

    junction_data,
    affected_junction

):

    source = junction_data[

        junction_data["junction"]

        == affected_junction

    ]

    if len(source) == 0:

        return None

    lat = source.iloc[0]["latitude"]

    lon = source.iloc[0]["longitude"]

    diversion_points = suggest_diversion(

        junction_data,

        affected_junction,

        top_n=3

    )

    m = folium.Map(

        location=[lat, lon],

        zoom_start=13

    )

    # Affected Junction

    folium.Marker(

        [lat, lon],

        popup=f"""
        Affected Junction:
        {affected_junction}
        """,

        icon=folium.Icon(
            color="red"
        )

    ).add_to(m)

    # Diversion Points

    for _, row in diversion_points.iterrows():

        folium.Marker(

            [

                row["latitude"],

                row["longitude"]

            ],

            popup=f"""
            Diversion Junction:
            {row['junction']}

            Risk:
            {row['risk_level']}

            Distance:
            {round(row['distance'],2)} km
            """,

            icon=folium.Icon(
                color="green"
            )

        ).add_to(m)

    return m


# -----------------------------------
# Diversion Statistics
# -----------------------------------

def diversion_statistics(

    junction_data

):

    distances = []

    for junction in junction_data[
        "junction"
    ].dropna():

        try:

            alt = suggest_diversion(

                junction_data,

                junction,

                top_n=3

            )

            if len(alt) > 0:

                distances.extend(

                    alt["distance"]

                    .tolist()

                )

        except:

            pass

    if len(distances) == 0:

        return {

            "average_distance": 0,

            "max_distance": 0,

            "min_distance": 0

        }

    return {

        "average_distance":

            round(

                sum(distances)

                /

                len(distances),

                2

            ),

        "max_distance":

            round(

                max(distances),

                2

            ),

        "min_distance":

            round(

                min(distances),

                2

            )

    }


# -----------------------------------
# Generate Diversion Table
# -----------------------------------

def generate_diversion_table(

    junction_data

):

    rows = []

    for junction in junction_data[
        "junction"
    ].dropna():

        try:

            alt = suggest_diversion(

                junction_data,

                junction,

                top_n=3

            )

            if len(alt) >= 3:

                rows.append({

                    "affected_junction":

                        junction,

                    "alternative_1":

                        alt.iloc[0][
                            "junction"
                        ],

                    "alternative_2":

                        alt.iloc[1][
                            "junction"
                        ],

                    "alternative_3":

                        alt.iloc[2][
                            "junction"
                        ]

                })

        except:

            pass

    return pd.DataFrame(rows)


# -----------------------------------
# Save Diversion CSV
# -----------------------------------

def save_diversion_table(

    junction_data,

    output_path=
    "data/diversion_recommendations.csv"

):

    diversion_df = (

        generate_diversion_table(

            junction_data

        )

    )

    diversion_df.to_csv(

        output_path,

        index=False

    )

    return diversion_df


# -----------------------------------
# Testing
# -----------------------------------

if __name__ == "__main__":

    df = load_junction_data()

    print("\nDataset Shape")

    print(df.shape)

    sample_junction = (

        df["junction"]

        .dropna()

        .iloc[0]

    )

    print(

        "\nSample Junction:",

        sample_junction

    )

    print(

        suggest_diversion(

            df,

            sample_junction

        )

    )