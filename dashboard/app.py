import streamlit as st
import pandas as pd
import os
import time

st.set_page_config(page_title="Traffic Dashboard", layout="wide")

st.title("🚦 Smart Traffic Monitoring Dashboard")

log_path = os.path.join(os.getcwd(), "outputs", "logs.csv")

if not os.path.exists(log_path):
    st.warning("Run main.py first")
    st.stop()

df = pd.read_csv(log_path)

if df.empty:
    st.warning("No data yet")
    st.stop()

# Convert time
df["Time"] = pd.to_datetime(df["Time"])

# ================= KPI =================
st.subheader("📊 Overview")

col1, col2 = st.columns(2)

with col1:
    st.metric("Total Violations", len(df))

with col2:
    st.metric("Unique IDs", df["TrackID"].nunique())

# ================= MAP =================
st.subheader("🗺️ Violation Map")

if "Lat" in df.columns and "Lon" in df.columns:
    map_df = df[["Lat", "Lon"]].rename(columns={"Lat": "lat", "Lon": "lon"})
    st.map(map_df)

# ================= CHART =================
st.subheader("📈 Violation Distribution")
st.bar_chart(df["Violation"].value_counts())

# ================= TABLE =================
st.subheader("📋 Logs")
st.dataframe(df.sort_values(by="Time", ascending=False), use_container_width=True)

# ================= IMAGES =================
st.subheader("📸 Evidence")

cols = st.columns(3)

recent = df.tail(6)

for i, (_, row) in enumerate(recent.iterrows()):
    img_path = row["Plate"]

    if isinstance(img_path, str) and os.path.exists(img_path):
        with cols[i % 3]:
            st.image(img_path, caption=f"{row['Violation']} | ID:{row['TrackID']}")

# ================= AUTO REFRESH =================
time.sleep(3)
st.rerun()
    #streamlit run dashboard/app.py