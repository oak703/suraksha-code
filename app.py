import os
import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="SurakshaCode - AI Fraud Defense", page_icon="🛡️", layout="wide")

st.title("🛡️ SurakshaCode")
st.caption("AI-Powered Financial Fraud & Scam Analyzer for Indian Digital Payments | Powered by BharatCode API")

# API Key Handling
api_key = os.getenv("BHARATCODE_API_KEY") or st.sidebar.text_input("Enter BharatCode API Key", type="password")

if not api_key:
    st.info("Please enter your BharatCode API key to start analyzing digital threats.")
    st.stop()

client = OpenAI(
    api_key=api_key,
    base_url="https://bharatcode.ai/api/model/v1"
)

# Application UI
st.subheader("🔍 Analyze Suspicious Activity")
source_type = st.radio("Select Scam/Threat Vector:", ["SMS / WhatsApp Message", "UPI Collect / Payment Request", "Voice Call Transcription"])
user_input = st.text_area("Paste suspicious text, UPI handle details, or communication here:", height=150)

def analyze_security_threat(text: str, category: str) -> str:
    system_prompt = (
        "You are SurakshaCode, an expert AI threat analyst specializing in Indian cyber fraud, "
        "UPI payment scams, phishing attempts, and deceptive digital communications across Indian regional contexts.\n\n"
        "Provide a structured security audit report in Markdown format containing:\n"
        "1. Threat Level: [SAFE / SUSPICIOUS / DANGEROUS HIGH-RISK]\n"
        "2. Scam Category: (e.g., Fake Electricity Bill, Unauthorized UPI Collect Request, Bank KYC Expiry, Fraudulent Job Offer)\n"
        "3. Risk Factors & Manipulation Tactics: Explain specific psychological tricks or technical red flags identified.\n"
        "4. Immediate Victim Action Plan: 3 clear step-by-step actions the user should take right now.\n"
        "5. Reporting Channels: Include official Indian cybercrime reporting info (e.g., National Cyber Crime Helpline 1930 / cybercrime.gov.in)."
    )

    response = client.chat.completions.create(
        model="qwen-3.8-27b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Category: {category}\nInput Content:\n{text}"}
        ],
        temperature=0.2,
        max_tokens=1500
    )
    return response.choices[0].message.content

if st.button("Run Suraksha Audit", type="primary"):
    if not user_input.strip():
        st.warning("Please paste some content to audit.")
    else:
        with st.spinner("Analyzing against Indian cyber threat patterns..."):
            report = analyze_security_threat(user_input, source_type)
            st.markdown("### 📋 Threat Analysis Report")
            st.markdown(report)
