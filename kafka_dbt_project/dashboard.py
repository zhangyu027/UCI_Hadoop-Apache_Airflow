import streamlit as st
import pandas as pd
import psycopg2

st.title("Kafka + dbt Sales Dashboard")

conn = psycopg2.connect(
    host="localhost",
    database="analytics",
    user="postgres",
    password="postgres",
    port=5432
)

raw_df = pd.read_sql("SELECT * FROM raw_sales", conn)
summary_df = pd.read_sql("SELECT * FROM sales_summary", conn)

st.header("Raw Sales Events")
st.dataframe(raw_df)

st.header("Sales Summary")
st.dataframe(summary_df)

st.bar_chart(summary_df.set_index("event")["total_events"])

conn.close()
