import streamlit as st
from datetime import datetime
import pandas as pd
import requests

API_URL = "https://expense-management-system-te4z.onrender.com"

def analytics_months_tab():
    st.title("Expense Breakdown by Months")

    try:
        response = requests.get(
            f"{API_URL}/monthly_summary/",
            timeout=30
        )

        # Check what the backend returned
        if response.status_code != 200:
            st.error(f"Backend error: HTTP {response.status_code}")
            st.code(response.text[:500])
            return

        try:
            monthly_summary = response.json()
        except requests.exceptions.JSONDecodeError:
            st.error("The backend returned a response that is not JSON.")
            st.code(response.text[:500])
            return

        df = pd.DataFrame(monthly_summary)

        if df.empty:
            st.info("No monthly expense data available yet.")
            return

        df.rename(columns={
            "expense_month": "Month Number",
            "month_name": "Month Name",
            "total": "Total"
        }, inplace=True)

        df_sorted = df.sort_values(
            by=["Month Number"], ascending=False
        )

        st.bar_chart(
            data=df_sorted.set_index("Month Name")["Total"],
            width="stretch",
            height="content"
        )

        df_sorted["Total"] = df_sorted["Total"].map("{:.2f}".format)
        st.table(df_sorted.set_index("Month Number"))

    except requests.exceptions.RequestException as e:
        st.error(f"Could not connect to the backend: {e}")