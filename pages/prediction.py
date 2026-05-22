import streamlit as st
import pandas as pd
import sqlite3
import joblib
import shap

st.set_page_config(page_title="Fraud Prediction", layout="wide")

model = joblib.load("models/fraud_model.pkl")

st.header("🔍 Fraud Prediction")

type_map = {
    "UPI": 0,
    "Credit Card": 1,
    "Bank Transfer": 2
}

tab1, tab2 = st.tabs(["Single Transaction", "Bulk CSV Upload"])

with tab1:
    amount = st.number_input("Transaction Amount", min_value=0)
    transaction_type = st.selectbox("Transaction Type", ["UPI", "Credit Card", "Bank Transfer"])
    device_risk = st.slider("Device Risk Score", 0, 100, 50)

    if st.button("Analyze Transaction"):
        input_data = pd.DataFrame(
            [[amount, type_map[transaction_type], device_risk]],
            columns=["amount", "transaction_type", "device_risk"]
        )

        prediction = model.predict(input_data)[0]
        probability = model.predict_proba(input_data)[0][1] * 100

        result = "Fraud" if prediction == 1 else "Safe"

        if result == "Fraud":
            st.error("🚨 Fraudulent Transaction Detected")
        else:
            st.success("✅ Safe Transaction")

        st.metric("Fraud Risk Score", f"{probability:.2f}%")

        st.subheader("🧠 AI Explainability")
        explainer = shap.TreeExplainer(model)
        shap_values = explainer(input_data)
        impact_scores = shap_values.values
        # Convert SHAP output safely into 1D values
        if impact_scores.ndim == 3:
            impact_scores = impact_scores[0, :, 1]
        elif impact_scores.ndim == 2:
            impact_scores = impact_scores[0]
        else:
            impact_scores = impact_scores.flatten()
        feature_importance = pd.DataFrame({
            "Feature": ["Amount", "Transaction Type", "Device Risk"],
            "Impact Score": impact_scores
        })
        st.write("The model considered these factors while making the prediction:")
        st.dataframe(feature_importance, use_container_width=True)
        st.bar_chart(feature_importance.set_index("Feature"))
        st.write("The model considered these factors while making the prediction:")
        st.dataframe(feature_importance, use_container_width=True)
        st.bar_chart(feature_importance.set_index("Feature"))

        st.subheader("🛡️ Security Recommendations")

        if probability >= 70:
            st.write("""
            - Enable multi-factor authentication
            - Temporarily block suspicious account activity
            - Verify user identity
            - Monitor transaction frequency
            - Alert cybersecurity team
            """)
        else:
            st.write("""
            - Continue regular monitoring
            - Maintain secure password practices
            - Keep fraud analytics active
            """)

        conn = sqlite3.connect("fraud_detection.db")
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL,
            transaction_type TEXT,
            device_risk INTEGER,
            prediction TEXT,
            fraud_score REAL
        )
        """)

        cursor.execute("""
        INSERT INTO transactions (
            amount, transaction_type, device_risk, prediction, fraud_score
        )
        VALUES (?, ?, ?, ?, ?)
        """, (
            amount,
            transaction_type,
            device_risk,
            result,
            probability
        ))

        conn.commit()
        conn.close()

        st.info("Transaction saved successfully.")

with tab2:
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
    st.info("CSV must contain: amount, transaction_type, device_risk")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        st.subheader("Uploaded Data")
        st.dataframe(df, use_container_width=True)

        if st.button("Analyze CSV"):
            df["transaction_type_encoded"] = df["transaction_type"].map(type_map)

            input_data = df[["amount", "transaction_type_encoded", "device_risk"]]
            input_data.columns = ["amount", "transaction_type", "device_risk"]

            predictions = model.predict(input_data)
            probabilities = model.predict_proba(input_data)[:, 1] * 100

            df["prediction"] = ["Fraud" if p == 1 else "Safe" for p in predictions]
            df["fraud_score"] = probabilities

            st.subheader("Prediction Results")
            st.dataframe(df, use_container_width=True)

            csv = df.to_csv(index=False)

            st.download_button(
                label="Download Analyzed CSV",
                data=csv,
                file_name="analyzed_fraud_results.csv",
                mime="text/csv"
            )