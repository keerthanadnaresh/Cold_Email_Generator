import streamlit as st
from extractor import extract_job_details
from portfolio import get_portfolio_links
from emailer import generate_cold_email

st.set_page_config(page_title="Cold Email Generator", layout="centered")
st.title("📧 Cold Email Generator")
st.markdown("Generate personalized cold emails based on job listings.")

url = st.text_input("🔗 Enter Careers Page URL")

if st.button("Generate Cold Email") and url:
    job_info = extract_job_details(url)
    if job_info:
        st.subheader("📝 Job Info")
        st.json(job_info)

        portfolio_links = get_portfolio_links(job_info["skills"])
        email = generate_cold_email(job_info, portfolio_links)

        st.subheader("📬 Generated Email")
        st.code(email)
    else:
        st.error("❌ Could not extract job info. Try another URL.")
