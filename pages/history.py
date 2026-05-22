import streamlit as st
import pandas as pd
import sqlite3
from fpdf import FPDF

st.set_page_config(page_title="Transaction History", layout="wide")

st.header("🕘 Transaction History")

conn = sqlite3.connect("fraud_detection.db")
df = pd.read_sql_query("SELECT * FROM transactions", conn)
conn.close()

def create_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Cyber Fraud Detection Report", ln=True, align="C")

    pdf.set_font("Arial", "", 12)
    pdf.ln(10)
    pdf.cell(0, 10, f"Total Transactions: {len(data)}", ln=True)
    pdf.cell(0, 10, f"Fraud Transactions: {len(data[data['prediction'] == 'Fraud'])}", ln=True)
    pdf.cell(0, 10, f"Safe Transactions: {len(data[data['prediction'] == 'Safe'])}", ln=True)
    pdf.cell(0, 10, f"Average Risk Score: {data['fraud_score'].mean():.2f}%", ln=True)

    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(25, 10, "ID", 1)
    pdf.cell(35, 10, "Amount", 1)
    pdf.cell(45, 10, "Type", 1)
    pdf.cell(35, 10, "Result", 1)
    pdf.cell(40, 10, "Risk Score", 1)
    pdf.ln()

    pdf.set_font("Arial", "", 10)

    for _, row in data.iterrows():
        pdf.cell(25, 10, str(row["id"]), 1)
        pdf.cell(35, 10, str(row["amount"]), 1)
        pdf.cell(45, 10, str(row["transaction_type"]), 1)
        pdf.cell(35, 10, str(row["prediction"]), 1)
        pdf.cell(40, 10, f"{row['fraud_score']:.2f}%", 1)
        pdf.ln()

    return pdf.output(dest="S").encode("latin-1")

if df.empty:
    st.warning("No transaction history found yet.")
else:
    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False)

    st.download_button(
        label="Download History as CSV",
        data=csv,
        file_name="fraud_transaction_history.csv",
        mime="text/csv"
    )

    pdf_data = create_pdf(df)

    st.download_button(
        label="Download PDF Report",
        data=pdf_data,
        file_name="cyber_fraud_report.pdf",
        mime="application/pdf"
    )