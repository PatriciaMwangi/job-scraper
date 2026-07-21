import streamlit as st
import pandas as pd

st.set_page_config(page_title="Nairobi Software Engineering Job Market", layout="wide")
st.title("📊 Nairobi Software Engineering Job Market Dashboard")
st.caption("Data scraped from myjobmag.co.ke — updated periodically")

try:
    df = pd.read_csv("jobs_clean.csv", parse_dates=["date_posted_clean"])
except FileNotFoundError:
    st.error("No data file found. Run the scraper locally first.")
    st.stop()

st.metric("Total Jobs Tracked", len(df))

tab1, tab2, tab3 = st.tabs(["📋 Raw Data", "📈 Charts", "🔍 Breakdown"])

with tab1:
    st.dataframe(df, use_container_width=True)

with tab2:
    col1, col2 = st.columns(2)
    col1.image("chart_top_companies.png", caption="Top Companies")
    col2.image("chart_postings_timeline.png", caption="Postings Over Time")
    st.image("chart_wordcloud.png", caption="Common Keywords")

with tab3:
    st.subheader("Seniority Breakdown")
    st.bar_chart(df["seniority"].value_counts())
    st.subheader("Work Mode Breakdown")
    st.bar_chart(df["work_mode"].value_counts())