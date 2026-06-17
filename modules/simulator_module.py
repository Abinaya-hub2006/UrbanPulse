import numpy as np


def simulate_event(
    event_cause,
    priority,
    road_closure,
    risk_level,
    duration_hours,
    crowd_size
):
    """
    What-If Event Simulator

    Returns:
    {
        response,
        impact_score,
        officers_range,
        barricades_range
    }
    """

    cause_score = {

        "vehicle_breakdown": 1,
        "pot_holes": 1,
        "construction": 2,
        "water_logging": 2,
        "road_conditions": 2,
        "tree_fall": 2,
        "accident": 3,
        "congestion": 3,
        "public_event": 4,
        "procession": 4,
        "vip_movement": 5,
        "protest": 5,
        "others": 1,
        "debris": 1

    }

    base = cause_score.get(
        str(event_cause).lower(),
        2
    )

    # Priority Impact
    if str(priority).lower() == "high":
        base += 2

    # Road Closure Impact
    if road_closure:
        base += 2

    # Historical Risk Multiplier
    risk_multiplier = {

        "Low": 1.0,
        "Medium": 1.3,
        "High": 1.6,
        "Critical": 2.0

    }

    base *= risk_multiplier.get(
        risk_level,
        1.0
    )

    # Crowd Scaling
    crowd_factor = (
        np.log1p(crowd_size)
        /
        np.log1p(1000)
    )

    # Duration Scaling
    duration_factor = (
        1 +
        duration_hours / 12
    )

    # Impact Score
    impact_score = (
        base *
        crowd_factor *
        duration_factor
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

    # Response Level

    if impact_score < 6:

        response = "Routine"

    elif impact_score < 12:

        response = "Urgent"

    else:

        response = "Critical"

    return {

        "response": response,

        "impact_score": float(
            round(
                impact_score,
                2
            )
        ),

        "officers_range":
            f"{officers_min}-{officers_max}",

        "barricades_range":
            f"{barricades_min}-{barricades_max}"

    }


def duration_sensitivity_analysis(
    event_cause,
    priority,
    road_closure,
    risk_level,
    crowd_size
):
    """
    Generates impact trend across durations
    """

    results = []

    for duration in [1, 2, 4, 6, 8]:

        result = simulate_event(
            event_cause,
            priority,
            road_closure,
            risk_level,
            duration,
            crowd_size
        )

        results.append({

            "duration_hours": duration,

            "impact_score":
                result["impact_score"]

        })

    return results


def crowd_sensitivity_analysis(
    event_cause,
    priority,
    road_closure,
    risk_level,
    duration_hours
):
    """
    Generates impact trend across crowd sizes
    """

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

            "crowd_size": crowd,

            "impact_score":
                result["impact_score"]

        })

    return results


if __name__ == "__main__":

    output = simulate_event(

        event_cause="procession",

        priority="High",

        road_closure=True,

        risk_level="Critical",

        duration_hours=4,

        crowd_size=5000

    )

    print(output)