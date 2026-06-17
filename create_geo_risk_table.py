import pandas as pd

risk_df = pd.read_csv(
    "data/junction_risk_table.csv"
)

event_df = pd.read_csv(
    "data/Astram_event_data.csv",
    engine="python",
    on_bad_lines="skip"
)

coords = (

    event_df

    .groupby("junction")

    .agg({

        "latitude":"mean",

        "longitude":"mean"

    })

    .reset_index()

)

final_df = risk_df.merge(

    coords,

    on="junction",

    how="left"

)

final_df.to_csv(

    "data/junction_risk_table.csv",

    index=False

)

print("Done")
print(final_df.columns)