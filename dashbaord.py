import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
file_path = 'Sustainability_KPI_Data.xlsx'
df = pd.read_excel(file_path, sheet_name='Sheet1')

# Set page configuration
st.set_page_config(page_title="Sustainability KPI Dashboard", layout="wide")

# Title
st.title("Sustainability KPI Dashboard")

# KPI Metrics
total_energy = df["Energy_Consumption_MtCO2e"].sum()
total_transportation = df["Transportation_MtCO2e"].sum()
total_waste = df["Waste_MtCO2e"].sum()

# KPI Row
with st.container():
    kpi1, kpi2, kpi3 = st.columns(3)
    with kpi1:
        st.metric(label="Energy Consumption (MTCO2e)", value=f"{total_energy:,.0f}", delta="Target: 257K")
    with kpi2:
        st.metric(label="Transportation (MTCO2e)", value=f"{total_transportation:,.0f}", delta="Target: 78K")
    with kpi3:
        st.metric(label="Waste (MTCO2e)", value=f"{total_waste:,.0f}", delta="Target: 34K")

# Main Graph Area
with st.container():
    # Emissions Over Time
    st.subheader("Emissions Over Time")
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.fill_between(df["Month"], df["Energy_Consumption_MtCO2e"], label="Energy", alpha=0.6, color="#7FC97F")
    ax.fill_between(df["Month"], df["Transportation_MtCO2e"], label="Transportation", alpha=0.6, color="#BEAED4")
    ax.fill_between(df["Month"], df["Waste_MtCO2e"], label="Waste", alpha=0.6, color="#FDC086")
    ax.set_xlabel("Month")
    ax.set_ylabel("MTCO2e")
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.5)
    st.pyplot(fig)

# Bottom Section with Pie Charts
with st.container():
    col1, col2, col3 = st.columns(3)

    # Emissions by Category
    with col1:
        st.subheader("Emissions by Category")
        categories = ["Energy", "Transportation", "Waste"]
        category_totals = [total_energy, total_transportation, total_waste]
        fig, ax = plt.subplots(figsize=(3, 3))
        ax.pie(category_totals, labels=categories, autopct='%1.1f%%', startangle=140, colors=["#7FC97F", "#BEAED4", "#FDC086"])
        st.pyplot(fig)

    # Emissions by Scope
    with col2:
        st.subheader("Emissions by Scope")
        scope_totals = [
            df["Scope_1_MtCO2e"].sum(),
            df["Scope_2_MtCO2e"].sum(),
            df["Scope_3_MtCO2e"].sum(),
        ]
        scope_labels = ["Scope 1", "Scope 2", "Scope 3"]
        fig, ax = plt.subplots(figsize=(3, 3))
        ax.pie(scope_totals, labels=scope_labels, autopct='%1.1f%%', startangle=140, colors=["#386CB0", "#F0027F", "#BF5B17"])
        st.pyplot(fig)
    
    # Empty Column Placeholder (for symmetry or future use)
    with col3:
        st.subheader("")
        st.write("")
