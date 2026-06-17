"""
Risk Intelligence Module

Module 1

Purpose:
- Load risk data
- Generate KPIs
- Risk distribution
- Critical junction analysis
- Heatmap support

Used by:
- Overview Page
- Risk Heatmap Page
"""

import pandas as pd


# -----------------------------------
# Load Risk Data
# -----------------------------------

def load_risk_data():

    df = pd.read_csv(
        "data/junction_risk_table.csv"
    )

    return df


# -----------------------------------
# KPI Metrics
# -----------------------------------

def get_kpis(df):

    total_junctions = len(df)

    critical_count = len(
        df[
            df["risk_level"]
            ==
            "Critical"
        ]
    )

    high_count = len(
        df[
            df["risk_level"]
            ==
            "High"
        ]
    )

    medium_count = len(
        df[
            df["risk_level"]
            ==
            "Medium"
        ]
    )

    low_count = len(
        df[
            df["risk_level"]
            ==
            "Low"
        ]
    )

    return {

        "total_junctions":
            total_junctions,

        "critical":
            critical_count,

        "high":
            high_count,

        "medium":
            medium_count,

        "low":
            low_count
    }


# -----------------------------------
# Risk Distribution
# -----------------------------------

def risk_distribution(df):

    dist = (

        df["risk_level"]

        .value_counts()

        .reset_index()

    )

    dist.columns = [

        "risk_level",

        "count"

    ]

    return dist


# -----------------------------------
# Critical Junctions
# -----------------------------------

def get_critical_junctions(df):

    critical = df[

        df["risk_level"]

        ==

        "Critical"

    ]

    return critical.sort_values(

        by="incident_count",

        ascending=False

    )


# -----------------------------------
# High Risk Junctions
# -----------------------------------

def get_high_risk_junctions(df):

    high = df[

        df["risk_level"]

        ==

        "High"

    ]

    return high.sort_values(

        by="incident_count",

        ascending=False

    )


# -----------------------------------
# Search Junction
# -----------------------------------

def search_junction(

    df,

    junction_name

):

    result = df[

        df["junction"]

        .str.contains(

            junction_name,

            case=False,

            na=False

        )

    ]

    return result


# -----------------------------------
# Risk Summary
# -----------------------------------

def get_risk_summary(df):

    summary = (

        df.groupby(

            "risk_level"

        )

        .agg({

            "incident_count":"mean",

            "high_priority_ratio":"mean",

            "road_closure_ratio":"mean"

        })

        .round(2)

    )

    return summary


# -----------------------------------
# Heatmap Data
# -----------------------------------

def get_heatmap_data(df):

    cols = [

        "junction",

        "latitude",

        "longitude",

        "risk_level"

    ]

    available_cols = [

        c

        for c in cols

        if c in df.columns

    ]

    return df[available_cols]


# -----------------------------------
# Risk Color Mapping
# -----------------------------------

def risk_color(risk_level):

    colors = {

        "Low": "#2ECC71",

        "Medium": "#F1C40F",

        "High": "#E67E22",

        "Critical": "#E74C3C"

    }

    return colors.get(

        risk_level,

        "#3498DB"

    )


# -----------------------------------
# Top N Critical Junctions
# -----------------------------------

def top_n_critical(

    df,

    n=10

):

    critical = get_critical_junctions(df)

    return critical.head(n)


# -----------------------------------
# Risk Statistics
# -----------------------------------

def get_statistics(df):

    stats = {

        "total_junctions":
            len(df),

        "critical":
            len(
                df[
                    df["risk_level"]
                    ==
                    "Critical"
                ]
            ),

        "high":
            len(
                df[
                    df["risk_level"]
                    ==
                    "High"
                ]
            ),

        "medium":
            len(
                df[
                    df["risk_level"]
                    ==
                    "Medium"
                ]
            ),

        "low":
            len(
                df[
                    df["risk_level"]
                    ==
                    "Low"
                ]
            )
    }

    return stats


# -----------------------------------
# Testing
# -----------------------------------

if __name__ == "__main__":

    df = load_risk_data()

    print("\nKPI Metrics")

    print(
        get_kpis(df)
    )

    print("\nDistribution")

    print(
        risk_distribution(df)
    )

    print("\nTop Critical Junctions")

    print(
        top_n_critical(df)
    )