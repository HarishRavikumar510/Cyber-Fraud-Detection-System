import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.set_page_config(page_title="Dashboard", layout="wide")

st.header("📊 Monitoring Dashboard")

conn = sqlite3.connect("fraud_detection.db")
df = pd.read_sql_query("SELECT * FROM transactions", conn)
conn.close()

if df.empty:
    st.warning("No data available. Make some predictions first.")
else:
    total_transactions = len(df)
    fraud_count = len(df[df["prediction"] == "Fraud"])
    safe_count = len(df[df["prediction"] == "Safe"])
    avg_risk = df["fraud_score"].mean()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Transactions", total_transactions)
    col2.metric("Fraud Detected", fraud_count)
    col3.metric("Safe Transactions", safe_count)
    col4.metric("Average Risk Score", f"{avg_risk:.2f}%")

    st.divider()

    col5, col6 = st.columns(2)

    with col5:
        st.subheader("Fraud vs Safe Distribution")
        pie_chart = px.pie(
            df,
            names="prediction",
            title="Transaction Classification"
        )
        st.plotly_chart(pie_chart, use_container_width=True)

    with col6:
        st.subheader("Transaction Type Analysis")
        bar_chart = px.histogram(
            df,
            x="transaction_type",
            color="prediction",
            title="Fraud by Transaction Type"
        )
        st.plotly_chart(bar_chart, use_container_width=True)

    st.subheader("Fraud Risk Score Trend")
    line_chart = px.line(
        df,
        y="fraud_score",
        markers=True,
        title="Risk Score Trend"
    )
    st.plotly_chart(line_chart, use_container_width=True)

    st.subheader("High Risk Transactions")
    high_risk = df[df["fraud_score"] >= 70]
    st.dataframe(high_risk, use_container_width=True)