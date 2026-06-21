import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_folium import st_folium
from modules.risk_module import *
from modules.resource_module import *
from modules.simulator_module import *
from modules.diversion_module import *
from modules.learning_module import *
from modules.retraining_module import *
import joblib

rf_model = joblib.load(
    "models/impact_model.pkl"
)

event_encoder = joblib.load(
    "models/event_encoder.pkl"
)

risk_encoder = joblib.load(
    "models/risk_encoder.pkl"
)
# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="UrbanPulse",
    page_icon="🚦",
    layout="wide"
)

# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

.main{
    background-color:#0b1220;
}

.block-container{
    padding-top:1rem;
    padding-bottom:1rem;
}

.hero-title{
    font-size:52px;
    font-weight:800;
    color:white;
}

.hero-sub{
    font-size:18px;
    color:#94a3b8;
    margin-bottom:20px;
}

.metric-card{
    background:#111827;
    padding:18px;
    border-radius:15px;
    border:1px solid #1f2937;
}

section[data-testid="stSidebar"]{
    background:#111827;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# LOAD DATA
# ==========================================

risk_df = load_risk_data()

# ==========================================
# HEADER
# ==========================================

st.markdown("""
<div class='hero-title'>
🚦 UrbanPulse
</div>

<div class='hero-sub'>
Event-Aware Traffic Intelligence Platform
</div>
""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR
# ==========================================

page = st.sidebar.radio(

    "Navigation",

    [

        "🏠 Command Center",

        "📍 Hotspot Intelligence",

        "🚓 Deployment Planner",

        "⚡ Scenario Simulator",

        "🛣 Diversion Control",

        "📈 System Analytics",

        "📡 Live Event Feed",

        "🧠 Learning Engine"

    ]
)

# ==========================================
# COMMAND CENTER
# ==========================================

if page == "🏠 Command Center":

    stats = get_statistics(risk_df)

    st.subheader("City Risk Overview")

    c1,c2,c3,c4 = st.columns(4)

    c1.metric(
        "Critical Junctions",
        stats["critical"]
    )

    c2.metric(
        "High Risk Areas",
        stats["high"]
    )

    c3.metric(
        "Total Junctions",
        stats["total_junctions"]
    )

    c4.metric(
        "Coverage Zones",
        10
    )

    st.markdown("---")

    st.subheader(
        "Bangalore Risk Map"
    )

    fig = px.scatter_mapbox(

        risk_df,

        lat="latitude",

        lon="longitude",

        color="risk_level",

        size="incident_count",

        hover_name="junction",

        zoom=10,

        height=650,

        mapbox_style="carto-darkmatter"

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader(
        "Top Critical Junctions"
    )

    st.dataframe(

        top_n_critical(

            risk_df,

            10

        ),

        use_container_width=True

    )
    # ==========================================
# HOTSPOT INTELLIGENCE
# ==========================================

elif page == "📍 Hotspot Intelligence":

    st.header("📍 Hotspot Intelligence")

    search = st.text_input(
        "Search Junction"
    )

    if search:

        result = search_junction(
            risk_df,
            search
        )

        st.subheader(
            "Search Results"
        )

        st.dataframe(
            result,
            use_container_width=True
        )

    st.markdown("---")

    st.subheader(
        "Critical Junction Leaderboard"
    )

    critical_df = get_critical_junctions(
        risk_df
    )

    st.dataframe(
        critical_df,
        use_container_width=True
    )

    fig = px.bar(

        critical_df.head(15),

        x="incident_count",

        y="junction",

        color="risk_level",

        orientation="h",

        title="Top 15 Critical Junctions"

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==========================================
# DEPLOYMENT PLANNER
# ==========================================

elif page == "🚓 Deployment Planner":

    st.header(
        "🚓 Deployment Planner"
    )

    event_cause = st.selectbox(

        "Event Cause",

        [

            "vehicle_breakdown",
            "construction",
            "water_logging",
            "accident",
            "congestion",
            "public_event",
            "procession",
            "vip_movement",
            "protest"

        ]

    )

    priority = st.selectbox(

        "Priority",

        [

            "Low",

            "High"

        ]

    )

    road_closure = st.checkbox(
        "Road Closure Required"
    )

    risk_level = st.selectbox(

        "Risk Level",

        [

            "Low",

            "Medium",

            "High",

            "Critical"

        ]

    )

    if st.button(
        "Generate Deployment Plan"
    ):

        result = recommend_resources(

            event_cause,

            priority,

            road_closure,

            risk_level

        )

        c1,c2,c3 = st.columns(3)

        c1.metric(

            "👮 Officers",

            result["officers_range"]

        )

        c2.metric(

            "🚧 Barricades",

            result["barricades_range"]

        )

        c3.metric(

            "⚠ Response",

            result["response_level"]

        )

        st.success(

            f"Deployment Score : {result['deployment_score']}"

        )

# ==========================================
# SCENARIO SIMULATOR
# ==========================================

elif page == "⚡ Scenario Simulator":

    st.header(
        "⚡ Scenario Simulator"
    )

    event_cause = st.selectbox(

        "Event Cause",

        [

            "vehicle_breakdown",
            "construction",
            "water_logging",
            "accident",
            "congestion",
            "public_event",
            "procession",
            "vip_movement",
            "protest"

        ],

        key="sim_cause"

    )

    priority = st.selectbox(

        "Priority",

        [

            "Low",

            "High"

        ],

        key="sim_priority"

    )

    risk_level = st.selectbox(

        "Risk Level",

        [

            "Low",

            "Medium",

            "High",

            "Critical"

        ],

        key="sim_risk"

    )

    road_closure = st.checkbox(

        "Road Closure",

        key="sim_closure"

    )

    duration = st.slider(

        "Duration (Hours)",

        1,

        12,

        4

    )

    crowd_size = st.slider(

        "Crowd Size",

        100,

        10000,

        5000

    )

    result = simulate_event(

        event_cause,

        priority,

        road_closure,

        risk_level,

        duration,

        crowd_size

    )

    st.success(

        f"Response Level : {result['response']}"

    )

    c1,c2,c3 = st.columns(3)

    c1.metric(

        "Impact Score",

        result["impact_score"]

    )

    c2.metric(

        "Officers",

        result["officers_range"]

    )

    c3.metric(

        "Barricades",

        result["barricades_range"]

    )

    st.markdown("---")

    duration_df = pd.DataFrame(

        duration_sensitivity_analysis(

            event_cause,

            priority,

            road_closure,

            risk_level,

            crowd_size

        )

    )

    fig1 = px.line(

        duration_df,

        x="duration_hours",

        y="impact_score",

        markers=True,

        title="Impact vs Duration"

    )

    st.plotly_chart(

        fig1,

        use_container_width=True

    )

    crowd_df = pd.DataFrame(

        crowd_sensitivity_analysis(

            event_cause,

            priority,

            road_closure,

            risk_level,

            duration

        )

    )

    fig2 = px.line(

        crowd_df,

        x="crowd_size",

        y="impact_score",

        markers=True,

        title="Impact vs Crowd Size"

    )

    st.plotly_chart(

        fig2,

        use_container_width=True

    )
    # ==========================================
# DIVERSION CONTROL
# ==========================================

elif page == "🛣 Diversion Control":

    st.header(
        "🛣 Diversion Control"
    )

    junction = st.selectbox(

        "Affected Junction",

        sorted(

            risk_df["junction"]

            .dropna()

            .unique()

        )

    )

    if st.button(
        "Generate Diversion Plan"
    ):

        st.session_state[
            "selected_junction"
        ] = junction

    if "selected_junction" in st.session_state:

        selected = st.session_state[
            "selected_junction"
        ]

        diversion_df = suggest_diversion(

            risk_df,

            selected,

            top_n=3

        )

        st.subheader(
            "Recommended Alternatives"
        )

        st.dataframe(

            diversion_df,

            use_container_width=True

        )

        # Risk Reduction

        risk_rank = {

            "Low": 1,

            "Medium": 2,

            "High": 3,

            "Critical": 4

        }

        try:

            current_risk = risk_df[

                risk_df["junction"]

                == selected

            ].iloc[0]["risk_level"]

            alt_risk = diversion_df.iloc[0][
                "risk_level"
            ]

            current_score = risk_rank[
                current_risk
            ]

            alt_score = risk_rank[
                alt_risk
            ]

            reduction = round(

                (

                    (current_score - alt_score)

                    /

                    current_score

                )

                * 100,

                1

            )

            st.success(

                f"Risk Reduction Potential : {reduction}%"

            )

        except:

            pass

        st.subheader(
            "Diversion Map"
        )

        try:

            diversion_map = create_diversion_map(

                risk_df,

                selected

            )

            st_folium(

                diversion_map,

                width=1200,

                height=600

            )

        except Exception as e:

            st.error(
                str(e)
            )

# ==========================================
# SYSTEM ANALYTICS
# ==========================================

elif page == "📈 System Analytics":

    st.header(
        "📈 System Analytics"
    )

    c1,c2 = st.columns(2)

    with c1:

        st.subheader(
            "Risk Distribution"
        )

        dist = risk_distribution(
            risk_df
        )

        fig = px.pie(

            dist,

            values="count",

            names="risk_level",

            hole=0.5

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    with c2:

        st.subheader(
            "Incident Distribution"
        )

        fig2 = px.histogram(

            risk_df,

            x="incident_count",

            nbins=20

        )

        st.plotly_chart(

            fig2,

            use_container_width=True

        )

    st.markdown("---")

    st.subheader(
        "Risk Summary"
    )

    st.dataframe(

        get_risk_summary(
            risk_df
        ),

        use_container_width=True

    )

    st.markdown("---")

    st.subheader(
        "Top 20 Junctions"
    )

    top20 = risk_df.sort_values(

        "incident_count",

        ascending=False

    ).head(20)

    fig3 = px.bar(

        top20,

        x="junction",

        y="incident_count",

        color="risk_level",

        title="Top Incident Junctions"

    )

    st.plotly_chart(

        fig3,

        use_container_width=True

    )
# ==========================================
# LIVE EVENT FEED
# ==========================================
elif page == "📡 Live Event Feed":

    st.header("📡 Live Event Feed")

    live_df = pd.read_csv(
        "data/live_events.csv"
    )

    # ==========================
    # KPIs
    # ==========================

    c1, c2 = st.columns(2)

    c1.metric(
        "Total Events",
        len(live_df)
    )

    c2.metric(
        "Active Events",
        len(
            live_df[
                live_df["status"] == "Live"
            ]
        )
    )

    st.dataframe(
        live_df,
        use_container_width=True
    )

    # ==========================
    # Active Events
    # ==========================

    st.markdown("## 🚨 Active Events")

    live_events = live_df[
        live_df["status"] == "Live"
    ]

    for _, row in live_events.iterrows():

        st.error(
            f"""
🔴 {row['event_name']}

📍 Location : {row['location']}

⚡ Event Type : {row['event_type']}

🕒 Status : {row['status']}
"""
        )

    st.markdown("---")

    # ==========================
    # Event Selection
    # ==========================

    selected_event = st.selectbox(
        "Select Event",
        live_df["event_name"]
    )

    event_row = live_df[
        live_df["event_name"]
        ==
        selected_event
    ].iloc[0]

    # ==========================
    # Event Details
    # ==========================

    st.markdown("## 📋 Event Details")

    d1, d2, d3 = st.columns(3)

    d1.metric(
        "Crowd Size",
        event_row["crowd_size"]
    )

    d2.metric(
        "Duration (Hours)",
        event_row["duration_hours"]
    )

    d3.metric(
        "Risk Level",
        event_row["risk_level"]
    )

    # ==========================
    # ML Forecast
    # ==========================

    result = simulate_event(

        event_row["event_type"],

        "High",

        True,

        event_row["risk_level"],

        event_row["duration_hours"],

        event_row["crowd_size"]

    )

    # ==========================
    # AI Reasoning
    # ==========================

    st.markdown("## 🧠 AI Reasoning")

    reason_df = pd.DataFrame({

        "Factor": [

            "Event Type",
            "Estimated Crowd",
            "Duration",
            "Risk Level"

        ],

        "Value": [

            event_row["event_type"],
            event_row["crowd_size"],
            event_row["duration_hours"],
            event_row["risk_level"]

        ]

    })

    st.table(reason_df)

    # ==========================
    # Forecast
    # ==========================

    st.markdown("## 🔮 Forecasted Impact")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Impact Score",
        result["impact_score"]
    )

    c2.metric(
        "Recommended Officers",
        result["officers_range"]
    )

    c3.metric(
        "Recommended Barricades",
        result["barricades_range"]
    )

    st.success(
        f"Recommended Response Level : {result['response']}"
    )

    # ==========================
    # Diversion Recommendation
    # ==========================

    st.markdown("## 🛣 Recommended Diversions")

    junction_df = load_junction_data()

    selected_junction = st.selectbox(

        "Select Affected Junction",

        junction_df["junction"]

    )

    diversions = suggest_diversion(

        junction_df,

        selected_junction

    )

    st.dataframe(

        diversions,

        use_container_width=True

    )

    # ==========================
    # Diversion Map
    # ==========================

    try:

        diversion_map = create_diversion_map(

            junction_df,

            selected_junction

        )

        st_folium(

            diversion_map,

            width=1200,

            height=500

        )

    except:

        st.warning(
            "Map could not be generated."
        )

elif page == "🧠 Learning Engine":

    st.header(
        "🧠 Post Event Learning Engine"
    )

    event_type = st.selectbox(

        "Event Type",

        [

            "procession",
            "vip_movement",
            "public_event",
            "construction",
            "accident"

        ]

    )

    crowd_size = st.number_input(

        "Crowd Size",

        min_value=100,

        value=1000

    )

    duration_hours = st.number_input(

        "Duration Hours",

        min_value=1,

        value=2

    )

    risk_level = st.selectbox(

        "Risk Level",

        [

            "Low",

            "Medium",

            "High",

            "Critical"

        ]

    )

    actual_impact = st.number_input(

        "Actual Impact Score",

        min_value=1.0,

        value=10.0

    )

    if st.button(

        "Save Review"

    ):

        add_review(

            event_type,

            crowd_size,

            duration_hours,

            risk_level,

            actual_impact

        )

        st.success(

            "Review Added"

        )

    st.markdown("---")

    reviews = load_reviews()

    st.subheader(

        "Historical Reviews"

    )

    st.dataframe(

        reviews,

        use_container_width=True

    )

    st.metric(

        "Total Reviews",

        len(reviews)

    )

    st.markdown("---")

    if st.button(

        "Retrain Model"

    ):

        total_records = retrain_model()

        st.success(

            f"Model Retrained Successfully using {total_records} records"

        )

# ==========================================
# FOOTER
# ==========================================

st.markdown("---")

st.caption(

    "UrbanPulse | Event-Aware Traffic Intelligence Platform | Flipkart Gridlock 2.0"

)
