import os
os.environ["STREAMLIT_CONFIG_DIR"] = "/tmp"
os.environ["STREAMLIT_HOME"] = "/tmp"
os.environ["STREAMLIT_DATA_DIR"] = "/tmp"
os.environ["STREAMLIT_STATIC_DIR"] = "/tmp"
os.environ["STREAMLIT_DISABLE_TELEMETRY"] = "true"
os.environ["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"

import zipfile
# Unzip Streamlit config if not already done
zip_path = "dotstreamlit_config.zip"
if os.path.exists(zip_path) and not os.path.exists(".streamlit"):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(".")


        
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Customer Spend Dashboard", layout="wide")

st.title("Transaction Dashboard")

# Load sample data
@st.cache_data
def load_data():
    try:
        url = "https://minh-analytics-projects.s3.amazonaws.com/transactions_data/synthetic_transactions.csv"
        return pd.read_csv(url, parse_dates=["timestamp"])
    except Exception as e:
        st.error(f"Failed to load data from S3: {e}")
        return pd.DataFrame()


df = load_data()

# Overview
st.subheader("Transaction Summary")
st.metric("Total Transactions", f"{len(df):,}")
st.metric("Total Spend", f"${df['amount'].sum():,.2f}")
st.metric("Unique Customers", df['customer_id'].nunique())

# Category spend
st.subheader("🧾 Spend by Category")
category_summary = df.groupby("category")["amount"].sum().sort_values(ascending=False)
st.bar_chart(category_summary)

# Fraud-like transactions
st.subheader("🚨 Potential Fraudulent Transactions")
threshold = st.slider("Show transactions over $", min_value=100.0, max_value=1000.0, value=500.0)
fraud_df = df[df["amount"] > threshold]
st.write(fraud_df.sort_values("amount", ascending=False).head(20))
