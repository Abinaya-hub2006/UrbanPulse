"""
Resource Recommendation Engine

Module 2

Purpose:
Recommend manpower, barricades and response level
based on event severity and historical risk.

Used by:
- Resource Planner Page
- What-If Simulator
"""



def recommend_resources(
    event_cause,
    priority,
    road_closure,
    risk_level
):

    """
    Returns:

    {
        officers_range,
        barricades_range,
        response_level,
        deployment_score
    }
    """

    # Event Severity

    cause_weights = {

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

    score = cause_weights.get(
        str(event_cause).lower(),
        2
    )

    # Priority Impact

    if str(priority).lower() == "high":

        score += 2

    # Road Closure Impact

    if road_closure:

        score += 2

    # Risk Level Impact

    risk_map = {

        "Low": 1.0,

        "Medium": 1.3,

        "High": 1.6,

        "Critical": 2.0

    }

    score *= risk_map.get(
        risk_level,
        1.0
    )

    deployment_score = round(
        score,
        2
    )

    # Officer Recommendation

    officers_mid = min(
        score * 2,
        35
    )

    officers_min = round(
        officers_mid * 0.8
    )

    officers_max = round(
        officers_mid * 1.2
    )

    # Barricade Recommendation

    barricades_mid = min(
        score * 3,
        60
    )

    barricades_min = round(
        barricades_mid * 0.8
    )

    barricades_max = round(
        barricades_mid * 1.2
    )

    # Response Level

    if score < 5:

        response = "Routine"

    elif score < 10:

        response = "Urgent"

    else:

        response = "Critical"

    return {

        "officers_range":
            f"{officers_min}-{officers_max}",

        "barricades_range":
            f"{barricades_min}-{barricades_max}",

        "response_level":
            response,

        "deployment_score":
            deployment_score
    }


def batch_recommendation(
    events
):

    """
    events = list of dicts

    Returns recommendations
    for multiple events
    """

    recommendations = []

    for event in events:

        result = recommend_resources(

            event["event_cause"],

            event["priority"],

            event["road_closure"],

            event["risk_level"]

        )

        recommendations.append({

            "event_cause":
                event["event_cause"],

            "risk_level":
                event["risk_level"],

            "officers":
                result["officers_range"],

            "barricades":
                result["barricades_range"],

            "response":
                result["response_level"]

        })

    return recommendations


def get_response_color(
    response_level
):

    """
    Streamlit helper
    """

    colors = {

        "Routine": "green",

        "Urgent": "orange",

        "Critical": "red"

    }

    return colors.get(
        response_level,
        "blue"
    )


if __name__ == "__main__":

    result = recommend_resources(

        event_cause="accident",

        priority="High",

        road_closure=True,

        risk_level="Critical"

    )

    print(result)