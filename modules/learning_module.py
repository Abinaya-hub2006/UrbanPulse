import pandas as pd
import os

FILE_PATH = "data/post_event_reviews.csv"

def load_reviews():

    return pd.read_csv(FILE_PATH)


def add_review(
    event_type,
    predicted_impact,
    actual_impact,
    predicted_officers,
    actual_officers,
    predicted_duration,
    actual_duration
):

    new_row = pd.DataFrame([{

        "event_type": event_type,

        "predicted_impact": predicted_impact,

        "actual_impact": actual_impact,

        "predicted_officers": predicted_officers,

        "actual_officers": actual_officers,

        "predicted_duration": predicted_duration,

        "actual_duration": actual_duration

    }])

    if os.path.exists(FILE_PATH):

        df = pd.read_csv(FILE_PATH)

        df = pd.concat(
            [df, new_row],
            ignore_index=True
        )

    else:

        df = new_row

    df.to_csv(
        FILE_PATH,
        index=False
    )

    return True


def calculate_accuracy(df):

    if len(df) == 0:

        return 0

    error = abs(

        df["actual_impact"]

        -

        df["predicted_impact"]

    )

    accuracy = (

        1 -

        (

            error.mean()

            /

            df["actual_impact"].mean()

        )

    ) * 100

    return round(
        accuracy,
        2
    )


def learning_insights(df):

    if len(df) == 0:

        return "No historical reviews available."

    df["impact_error"] = (

        df["actual_impact"]

        -

        df["predicted_impact"]

    )

    avg_error = round(

        df["impact_error"]

        .mean(),

        2

    )

    if avg_error > 2:

        return (
            "UrbanPulse is underestimating event impact. "
            "Increase future deployment recommendations."
        )

    elif avg_error < -2:

        return (
            "UrbanPulse is overestimating impact. "
            "Resources may be reduced."
        )

    else:

        return (
            "Predictions are aligned with actual outcomes."
        )