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

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Energy Consumption (MTCO2e)", value=f"{total_energy:,.0f}", delta="Target: 257K")
with col2:
    st.metric(label="Transportation (MTCO2e)", value=f"{total_transportation:,.0f}", delta="Target: 78K")
with col3:
    st.metric(label="Waste (MTCO2e)", value=f"{total_waste:,.0f}", delta="Target: 34K")

# Emissions Over Time (Line Chart)
st.subheader("Emissions Over Time")
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(df["Month"], df["Energy_Consumption_MtCO2e"], label="Energy", marker='o')
ax.plot(df["Month"], df["Transportation_MtCO2e"], label="Transportation", marker='o')
ax.plot(df["Month"], df["Waste_MtCO2e"], label="Waste", marker='o')
ax.set_xlabel("Month")
ax.set_ylabel("MTCO2e")
ax.legend()
ax.grid(True)
st.pyplot(fig)

# Emissions by Category (Pie Chart)
st.subheader("Emissions by Category")
categories = ["Energy_Consumption_MtCO2e", "Transportation_MtCO2e", "Waste_MtCO2e"]
category_totals = [total_energy, total_transportation, total_waste]
fig, ax = plt.subplots(figsize=(5, 5))
ax.pie(category_totals, labels=["Energy", "Transportation", "Waste"], autopct='%1.1f%%', startangle=140)
st.pyplot(fig)

# Emissions by Scope (Pie Chart)
st.subheader("Emissions by Scope")
scope_totals = [
    df["Scope_1_MtCO2e"].sum(),
    df["Scope_2_MtCO2e"].sum(),
    df["Scope_3_MtCO2e"].sum(),
]
fig, ax = plt.subplots(figsize=(5, 5))
ax.pie(scope_totals, labels=["Scope 1", "Scope 2", "Scope 3"], autopct='%1.1f%%', startangle=140)
st.pyplot(fig)
