import streamlit as st
import pandas as pd
import plotly.express as px
import json

st.set_page_config(
    page_title="Move More, Live Better",
    page_icon="🏃‍♂️",
    layout="centered"
)

# Load Data
@st.cache_data
def load_data():
    main_df = pd.read_excel('Level_1.xlsx')
    lookup_df = pd.read_excel('lookups.xlsx')
    return main_df, lookup_df

df, lookup = load_data()

# Merge Dataset
lookup = lookup.rename(columns={
    "lookup_id": "small_area",
    "area_name": "area_name"
})

df = df.merge(lookup, on="small_area", how="left")
df["area_name"] = df["local_authority"]

# Title
st.title("🚶 Move More, Live Better")
st.subheader("Climate Action Through Active Mobility and Its Co-Benefits")

st.markdown("""
Climate action is often perceived as costly and abstract.  
This interactive story shows how **active mobility**—walking and cycling—  
delivers **immediate health and environmental benefits**.
""")

st.divider()

# Map Section
st.header("🗺️ Spatial Overview of Physical Activity")

st.markdown("""
This interactive map illustrates how physical activity levels across different areas. Each point represents a local area, where larger and darker markers indicate higher levels of walking and cycling.
""")

with open("local-authority-district.geojson") as f:
    geojson = json.load(f)

map_fig = px.choropleth_mapbox(
    df,
    geojson=geojson,
    locations="area_name",
    featureidkey="properties.name",
    color="sum",                     
    mapbox_style="carto-positron",
    zoom=5,
    center={"lat": 54, "lon": -2},
    opacity=0.7,
    height=500
)

map_fig.update_layout(
    mapbox_style="carto-positron",
    margin={"r": 0, "t": 0, "l": 0, "b": 0}
)

st.plotly_chart(map_fig, use_container_width=True)
st.divider()

# =============================
# Visualization
# =============================
st.header("Most Areas Still Have Low Physical Activity Levels")

st.markdown(""" Most regions show relatively low levels of physical activity, reflecting a strong dependence on motorized transport. """)

fig1 = px.histogram(
    df,
    x="physical_activity",
    nbins=30,
    title="Distribution of Physical Activity Levels",
    labels={"physical_activity": "Physical Activity Index"},
    color_discrete_sequence=["#415ACA"]
)

st.plotly_chart(fig1, use_container_width=True)
st.divider()
# =============================

st.header("Active Mobility as a Simple Climate Action")

st.markdown(""" Walking and cycling represent some of the simplest and most accessible forms of climate action. 
            This relationship indicates that encouraging walking and cycling can help reduce air pollution, especially emissions associated with private vehicle use.
            """)

top_pa = df.sort_values("physical_activity", ascending=False).head(15)

fig2 = px.bar(
    top_pa,
    x="area_name",
    y="physical_activity",
    title="Top Areas by Physical Activity Level",
    labels={
        "area_name": "Area",
        "physical_activity": "Physical Activity Index"
    },
    color="physical_activity",
    color_discrete_sequence=["#415ACA"]
)

st.plotly_chart(fig2, use_container_width=True)
st.divider()

# =============================
st.header("Higher Physical Activity Is Linked to Better Air Quality")

st.markdown(""" Areas with higher levels of walking and cycling tend to experience better air quality. 
            This suggests that promoting active mobility can lead to significant air quality improvements, benefiting public health and the environment.
            """)

fig3 = px.scatter(
    df,
    x="physical_activity",
    y="air_quality",
    trendline="ols",
    title="Physical Activity vs Air Quality",
    labels={
        "physical_activity": "Physical Activity Index",
        "air_quality": "Air Quality Co-Benefit Index"
    },
    hover_data=["area_name"],
    color="physical_activity",
    color_discrete_sequence=["#415ACA"]
)

st.plotly_chart(fig3, use_container_width=True)
st.divider()

# =============================
st.header("Active Areas Experience Lower Environmental Noise")

st.markdown(""" There is a clear correlation between higher physical activity levels and reduced environmental noise. 
            This indicates that promoting walking and cycling can contribute to quieter, more peaceful urban environments.
            """)

fig4 = px.scatter(
    df,
    x="physical_activity",
    y="noise",
    trendline="ols",
    title="Physical Activity vs Noise Levels",
    labels={
        "physical_activity": "Physical Activity Index",
        "noise": "Noise Co-Benefit Index"
    },
    hover_data=["area_name"],
    color="physical_activity",
    color_discrete_sequence=["#415ACA"]
)

st.plotly_chart(fig4, use_container_width=True)
st.divider()

# =============================
st.header("Climate Action That Improves Quality of Life")

st.markdown(""" Encouraging walking and cycling not only helps combat climate change but also enhances air quality and reduces noise pollution.  
            These co-benefits contribute to healthier, more livable communities. 
            """)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Avg Physical Activity", f"{df['physical_activity'].mean():.2f}")

with col2:
    st.metric("Avg Air Quality Benefit", f"{df['air_quality'].mean():.2f}")

with col3:
    st.metric("Avg Noise Reduction", f"{df['noise'].mean():.2f}")

st.markdown("""
By integrating spatial context, the results show that **active mobility policies**  
can deliver **local, tangible benefits**—cleaner air, quieter streets,  
and healthier communities.
""")


st.divider()
