import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt

# Load data
file_path = 'Combined_Sustainability_KPI_Data.xlsx'
df = pd.read_excel(file_path)

# Set page configuration
st.set_page_config(page_title="Sustainability KPI Dashboard", layout="wide")

# Add custom styling
st.markdown("""
    <style>
        .metric-container {
            background-color: #f7f7f7;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        }
        .metric-title {
            font-size: 18px;
            font-weight: bold;
        }
        .progress-bar-red > div {
            background-color: #FF4D4F !important;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 style='text-align: center; margin-bottom: 30px;'>Sustainability KPI Dashboard</h1>", unsafe_allow_html=True)

# Dropdown for Year Selection
selected_year = st.selectbox("Select Year:", options=df['Year'].unique())
filtered_df = df[df['Year'] == selected_year]

# Dynamic Target Sliders
st.sidebar.header("Adjust Targets")
energy_target = st.sidebar.slider("Energy Target (MTCO2e)", min_value=200000, max_value=300000, value=257000, step=5000)
transportation_target = st.sidebar.slider("Transportation Target (MTCO2e)", min_value=50000, max_value=120000, value=95000, step=5000)
waste_target = st.sidebar.slider("Waste Target (MTCO2e)", min_value=20000, max_value=50000, value=40000, step=1000)

# KPI Metrics with Progress Bars
total_energy = filtered_df["Energy_Consumption_MtCO2e"].sum()
total_transportation = filtered_df["Transportation_MtCO2e"].sum()
total_waste = filtered_df["Waste_MtCO2e"].sum()

with st.container():
    col1, col2, col3 = st.columns(3)

    # Energy Consumption
    with col1:
        st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
        st.markdown("<p class='metric-title'>Energy Consumption</p>", unsafe_allow_html=True)
        st.metric(label="MTCO2e", value=f"{total_energy:,.0f}")
        if total_energy > energy_target:
            st.markdown("<div class='progress-bar-red'>", unsafe_allow_html=True)
            st.progress(1.0)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.progress(total_energy / energy_target)  # Cap at 1.0
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Transportation
    with col2:
        st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
        st.markdown("<p class='metric-title'>Transportation</p>", unsafe_allow_html=True)
        st.metric(label="MTCO2e", value=f"{total_transportation:,.0f}")
        if total_transportation > transportation_target:
            st.markdown("<div class='progress-bar-red'>", unsafe_allow_html=True)
            st.progress(1.0)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.progress(total_transportation / transportation_target)  # Cap at 1.0
        st.markdown("</div>", unsafe_allow_html=True)

    # Waste
    with col3:
        st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
        st.markdown("<p class='metric-title'>Waste</p>", unsafe_allow_html=True)
        st.metric(label="MTCO2e", value=f"{total_waste:,.0f}")
        if total_waste > waste_target:
            st.markdown("<div class='progress-bar-red'>", unsafe_allow_html=True)
            st.progress(1.0)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.progress(total_waste / waste_target)  # Cap at 1.0
        st.markdown("</div>", unsafe_allow_html=True)

# Toggle for Graph Visibility
show_emissions = st.checkbox("Show Emissions Over Time", value=True)
show_category_pie = st.checkbox("Show Emissions by Category", value=True)
show_scope_pie = st.checkbox("Show Emissions by Scope", value=True)

# Interactive Graphs
with st.container():
    if show_emissions:
        st.markdown("<h3>Emissions Over Time</h3>", unsafe_allow_html=True)
        # Prepare the data for Altair
        emissions_data = filtered_df.melt(
            id_vars=["Month"], 
            value_vars=["Energy_Consumption_MtCO2e", "Transportation_MtCO2e", "Waste_MtCO2e"],
            var_name="Category", 
            value_name="Emissions"
        )
        # Create the Altair chart
        chart = alt.Chart(emissions_data).mark_area(opacity=0.6).encode(
            x=alt.X('Month:N', title='Month', sort=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]),
            y=alt.Y('Emissions:Q', title='MTCO2e'),
            color=alt.Color('Category:N', scale=alt.Scale(scheme='category10'), legend=alt.Legend(title="Category"))
        ).properties(width=600, height=300)
        st.altair_chart(chart)

    col1, col2 = st.columns(2)

    # Emissions by Category
    if show_category_pie:
        with col1:
            st.markdown("<h3>Emissions by Category</h3>", unsafe_allow_html=True)
            categories = ["Energy", "Transportation", "Waste"]
            category_totals = [total_energy, total_transportation, total_waste]
            fig, ax = plt.subplots(figsize=(3, 3))
            ax.pie(category_totals, labels=categories, autopct='%1.1f%%', startangle=140, colors=["#7FC97F", "#BEAED4", "#FDC086"])
            st.pyplot(fig)

    # Emissions by Scope
    if show_scope_pie:
        with col2:
            st.markdown("<h3>Emissions by Scope</h3>", unsafe_allow_html=True)
            scope_totals = [
                filtered_df["Scope_1_MtCO2e"].sum(),
                filtered_df["Scope_2_MtCO2e"].sum(),
                filtered_df["Scope_3_MtCO2e"].sum(),
            ]
            scope_labels = ["Scope 1", "Scope 2", "Scope 3"]
            fig, ax = plt.subplots(figsize=(3, 3))
            ax.pie(scope_totals, labels=scope_labels, autopct='%1.1f%%', startangle=140, colors=["#386CB0", "#F0027F", "#BF5B17"])
            st.pyplot(fig)
