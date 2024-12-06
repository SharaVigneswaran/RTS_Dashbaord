import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
file_path = 'Sustainability_KPI_Data.xlsx'
df = pd.read_excel(file_path, sheet_name='Sheet1')

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
        .progress-bar {
            background-color: #e8e8e8;
            border-radius: 5px;
            padding: 5px;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 style='text-align: center; margin-bottom: 30px;'>🌱 Sustainability KPI Dashboard</h1>", unsafe_allow_html=True)

# KPI Metrics with Progress Bars
total_energy = df["Energy_Consumption_MtCO2e"].sum()
total_transportation = df["Transportation_MtCO2e"].sum()
total_waste = df["Waste_MtCO2e"].sum()

energy_target = 257000
transportation_target = 95000
waste_target = 40000

# KPI Container
with st.container():
    col1, col2, col3 = st.columns(3)

    # Energy Consumption
    with col1:
        st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
        st.markdown("<p class='metric-title'>Energy Consumption</p>", unsafe_allow_html=True)
        st.metric(label="MTCO2e", value=f"{total_energy:,.0f}")
        st.progress(min(total_energy / energy_target, 1.0))  # Cap at 1.0
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Transportation
    with col2:
        st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
        st.markdown("<p class='metric-title'>Transportation</p>", unsafe_allow_html=True)
        st.metric(label="MTCO2e", value=f"{total_transportation:,.0f}")
        st.progress(min(total_transportation / transportation_target, 1.0))  # Cap at 1.0
        st.markdown("</div>", unsafe_allow_html=True)

    # Waste
    with col3:
        st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
        st.markdown("<p class='metric-title'>Waste</p>", unsafe_allow_html=True)
        st.metric(label="MTCO2e", value=f"{total_waste:,.0f}")
        st.progress(min(total_waste / waste_target, 1.0))  # Cap at 1.0
        st.markdown("</div>", unsafe_allow_html=True)

# Graphs in a Compact Layout
with st.container():
    col1, col2, col3 = st.columns([2, 1, 1])

    # Emissions Over Time
    with col1:
        st.markdown("<h3 style='margin-top: 20px;'> Emissions Over Time</h3>", unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.fill_between(df["Month"], df["Energy_Consumption_MtCO2e"], label="Energy", alpha=0.6, color="#7FC97F")
        ax.fill_between(df["Month"], df["Transportation_MtCO2e"], label="Transportation", alpha=0.6, color="#BEAED4")
        ax.fill_between(df["Month"], df["Waste_MtCO2e"], label="Waste", alpha=0.6, color="#FDC086")
        ax.set_xlabel("Month", fontsize=12)
        ax.set_ylabel("MTCO2e", fontsize=12)
        ax.legend(fontsize=10)
        ax.grid(True, linestyle="--", alpha=0.5)
        st.pyplot(fig)

    # Emissions by Category
    with col2:
        st.markdown("<h3 style='margin-top: 20px;'> Emissions by Category</h3>", unsafe_allow_html=True)
        categories = ["Energy", "Transportation", "Waste"]
        category_totals = [total_energy, total_transportation, total_waste]
        fig, ax = plt.subplots(figsize=(3, 3))
        ax.pie(category_totals, labels=categories, autopct='%1.1f%%', startangle=140, colors=["#7FC97F", "#BEAED4", "#FDC086"])
        st.pyplot(fig)

    # Emissions by Scope
    with col3:
        st.markdown("<h3 style='margin-top: 20px;'> Emissions by Scope</h3>", unsafe_allow_html=True)
        scope_totals = [
            df["Scope_1_MtCO2e"].sum(),
            df["Scope_2_MtCO2e"].sum(),
            df["Scope_3_MtCO2e"].sum(),
        ]
        scope_labels = ["Scope 1", "Scope 2", "Scope 3"]
        fig, ax = plt.subplots(figsize=(3, 3))
        ax.pie(scope_totals, labels=scope_labels, autopct='%1.1f%%', startangle=140, colors=["#386CB0", "#F0027F", "#BF5B17"])
        st.pyplot(fig)
