import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

# Page config
st.set_page_config(page_title="Ad Campaign Dashboard", layout="wide")

# Title
st.title("📊 Ad Campaign Performance Dashboard")
st.markdown("Real-time insights for data-driven media buying decisions")

# --- Generate sample data (replace with real data later) ---
@st.cache_data
def load_data():
    np.random.seed(42)
    dates = pd.date_range(start="2026-01-01", end="2026-06-22", freq="D")
    
    channels = ["Meta Ads", "Google Ads", "TikTok Ads", "LinkedIn Ads"]
    data = []
    
    for date in dates:
        for channel in channels:
            spend = np.random.uniform(100, 1000)
            impressions = np.random.randint(10000, 100000)
            clicks = impressions * np.random.uniform(0.01, 0.05)
            conversions = clicks * np.random.uniform(0.02, 0.08)
            revenue = conversions * np.random.uniform(30, 100)
            
            data.append({
                "Date": date,
                "Channel": channel,
                "Spend": round(spend, 2),
                "Impressions": int(impressions),
                "Clicks": int(clicks),
                "Conversions": int(conversions),
                "Revenue": round(revenue, 2)
            })
    
    df = pd.DataFrame(data)
    
    # Calculate derived metrics
    df["CTR"] = (df["Clicks"] / df["Impressions"] * 100).round(2)
    df["CPC"] = (df["Spend"] / df["Clicks"]).round(2)
    df["CPA"] = (df["Spend"] / df["Conversions"]).round(2)
    df["ROAS"] = (df["Revenue"] / df["Spend"]).round(2)
    
    return df

df = load_data()

# --- Sidebar filters ---
st.sidebar.header("🔍 Filters")

channels = st.sidebar.multiselect(
    "Select Channels",
    options=df["Channel"].unique(),
    default=df["Channel"].unique()
)

date_range = st.sidebar.date_input(
    "Date Range",
    value=(df["Date"].min(), df["Date"].max()),
    min_value=df["Date"].min(),
    max_value=df["Date"].max()
)

# Filter data
filtered_df = df[
    (df["Channel"].isin(channels)) &
    (df["Date"] >= pd.to_datetime(date_range[0])) &
    (df["Date"] <= pd.to_datetime(date_range[1]))
]

# --- KPI Cards ---
col1, col2, col3, col4 = st.columns(4)

total_spend = filtered_df["Spend"].sum()
total_revenue = filtered_df["Revenue"].sum()
total_conversions = filtered_df["Conversions"].sum()
avg_roas = filtered_df["ROAS"].mean()

with col1:
    st.metric("💰 Total Spend", f"${total_spend:,.0f}")
with col2:
    st.metric("📈 Total Revenue", f"${total_revenue:,.0f}")
with col3:
    st.metric("🎯 Total Conversions", f"{total_conversions:,.0f}")
with col4:
    st.metric("📊 Avg ROAS", f"{avg_roas:.2f}x")

# --- Charts ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Spend & Revenue by Channel")
    channel_metrics = filtered_df.groupby("Channel")[["Spend", "Revenue"]].sum().reset_index()
    fig = px.bar(
        channel_metrics,
        x="Channel",
        y=["Spend", "Revenue"],
        barmode="group",
        text_auto=True
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🎯 ROAS by Channel")
    channel_roas = filtered_df.groupby("Channel")["ROAS"].mean().reset_index()
    fig = px.bar(
        channel_roas,
        x="Channel",
        y="ROAS",
        color="ROAS",
        color_continuous_scale="Viridis",
        text_auto=True
    )
    st.plotly_chart(fig, use_container_width=True)

# --- Time Series ---
st.subheader("📉 Daily Performance Trends")
daily_metrics = filtered_df.groupby("Date")[["Spend", "Revenue", "Conversions"]].sum().reset_index()

fig = px.line(
    daily_metrics,
    x="Date",
    y=["Spend", "Revenue"],
    title="Daily Spend vs Revenue"
)
st.plotly_chart(fig, use_container_width=True)

# --- Detailed Data Table ---
with st.expander("📋 View Detailed Data"):
    st.dataframe(filtered_df, use_container_width=True)

# --- Download CSV ---
@st.cache_data
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

csv = convert_df_to_csv(filtered_df)
st.download_button(
    label="📥 Download Data as CSV",
    data=csv,
    file_name="ad_campaign_data.csv",
    mime="text/csv"
)

# --- Footer ---
st.markdown("---")
st.caption("Built with ❤️ by Harrison Madu – Data & Growth Analytics")