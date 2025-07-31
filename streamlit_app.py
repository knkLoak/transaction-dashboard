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
        url = "https://minh-analytics-projects.s3.amazonaws.com/transactions_data/Synthetic_Transactions_Data.csv"
        return pd.read_csv(url, parse_dates=["timestamp"])
    except Exception as e:
        st.error(f"Failed to load data from S3: {e}")
        return pd.DataFrame()


df = load_data()

# Overview
st.subheader("Transaction Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Total Transactions", f"{len(df):,}")
col2.metric("Total Spend", f"${df['amount'].sum():,.2f}")
col3.metric("Unique Customers", df['customer_id'].nunique())

# Interactve filter
st.sidebar.header("Filters")
selected_category = st.sidebar.multiselect("Category", df["category"].unique())
selected_customer = st.sidebar.multiselect("Customer ID", df["customer_id"].unique().astype(str))

filtered_df = df.copy()
if selected_category:
    filtered_df = filtered_df[filtered_df["category"].isin(selected_category)]
if selected_customer:
    filtered_df = filtered_df[filtered_df["customer_id"].astype(str).isin(selected_customer)]

df = filtered_df  # update global df for the rest of the app

# Category spend
st.subheader("🧾 Spend by Category")
category_summary = df.groupby("category")["amount"].sum().sort_values(ascending=False)
st.bar_chart(category_summary)

# Fraud-like transactions
st.subheader("🚨 Potential Fraudulent Transactions")
threshold = st.slider("Show transactions over $", min_value=100.0, max_value=1000.0, value=500.0)
fraud_df = df[df["amount"] > threshold]
st.write(fraud_df.sort_values("amount", ascending=False).head(20))
