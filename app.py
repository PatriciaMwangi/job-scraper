import streamlit as st
import asyncio
import pandas as pd
from PIL import Image

# Import your existing scripts as modules
import scrape
import clean_job
import analyze_jobs
import visualize_jobs

st.set_page_config(page_title="MyJobMag Scraper Dashboard", layout="wide")
st.title("📊 Job Market Dashboard — Nairobi Software Engineering")

# --- Sidebar controls ---
st.sidebar.header("Pipeline Steps")

# 1. SCRAPE
if st.sidebar.button("1️⃣ Run Scraper"):
    with st.spinner("Scraping myjobmag.co.ke..."):
        jobs = asyncio.run(scrape.scrape_myjobmag("software engineering", "Nairobi"))
        existing_urls = scrape.load_existing_urls(scrape.CSV_FILE)
        new_count = scrape.append_jobs_to_csv(scrape.CSV_FILE, jobs, existing_urls)
    st.success(f"Scraped {len(jobs)} listings — {new_count} new, {len(jobs) - new_count} duplicates skipped")

# 2. CLEAN
if st.sidebar.button("2️⃣ Clean & Structure Data"):
    with st.spinner("Cleaning data..."):
        clean_job.main()
    st.success("Data cleaned — saved to jobs_clean.csv")

# 3. VISUALIZE (analyze + generate charts)
if st.sidebar.button("3️⃣ Analyze & Visualize"):
    with st.spinner("Generating charts..."):
        visualize_jobs.main()
    st.success("Charts generated")

st.divider()

# --- Main display area ---
tab1, tab2, tab3 = st.tabs(["📋 Raw Data", "📈 Charts", "🔍 Analysis Summary"])

with tab1:
    try:
        df = pd.read_csv("jobs_clean.csv")
        st.dataframe(df, use_container_width=True)
    except FileNotFoundError:
        st.info("No cleaned data yet — run steps 1 and 2 first.")

with tab2:
    col1, col2 = st.columns(2)
    try:
        col1.image("chart_top_companies.png", caption="Top Companies")
        col2.image("chart_postings_timeline.png", caption="Postings Over Time")
        st.image("chart_wordcloud.png", caption="Common Keywords")
    except FileNotFoundError:
        st.info("No charts yet — run step 3 first.")

with tab3:
    try:
        df = pd.read_csv("jobs_clean.csv", parse_dates=["date_posted_clean"])
        st.subheader("Top Companies")
        st.bar_chart(df["company"].value_counts().head(10))

        st.subheader("Seniority Breakdown")
        st.bar_chart(df["seniority"].value_counts())

        st.subheader("Work Mode Breakdown")
        st.bar_chart(df["work_mode"].value_counts())
    except FileNotFoundError:
        st.info("No data yet.")