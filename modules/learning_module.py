import pandas as pd

FILE_PATH = "data/post_event_reviews.csv"


def load_reviews():

    return pd.read_csv(FILE_PATH)


def add_review(
    event_type,
    crowd_size,
    duration_hours,
    risk_level,
    actual_impact
):

    df = load_reviews()

    new_row = {

        "event_type": event_type,
        "crowd_size": crowd_size,
        "duration_hours": duration_hours,
        "risk_level": risk_level,
        "actual_impact": actual_impact

    }

    df.loc[len(df)] = new_row

    df.to_csv(
        FILE_PATH,
        index=False
    )