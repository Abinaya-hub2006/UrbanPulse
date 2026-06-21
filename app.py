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

    predicted_impact = st.number_input(
        "Predicted Impact"
    )

    actual_impact = st.number_input(
        "Actual Impact"
    )

    predicted_officers = st.number_input(
        "Predicted Officers"
    )

    actual_officers = st.number_input(
        "Actual Officers Used"
    )

    predicted_duration = st.number_input(
        "Predicted Duration"
    )

    actual_duration = st.number_input(
        "Actual Duration"
    )

    if st.button(
        "Save Review"
    ):

        add_review(

            event_type,

            predicted_impact,

            actual_impact,

            predicted_officers,

            actual_officers,

            predicted_duration,

            actual_duration

        )

        st.success(
            "Review Stored Successfully"
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

    accuracy = calculate_accuracy(
        reviews
    )

    st.metric(
        "Prediction Accuracy",
        f"{accuracy}%"
    )

    st.info(

        learning_insights(
            reviews
        )

    )

# ==========================================
# FOOTER
# ==========================================

st.markdown("---")

st.caption(

    "UrbanPulse | Event-Aware Traffic Intelligence Platform | Flipkart Gridlock 2.0"

)
