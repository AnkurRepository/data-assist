import pandas as pd
import streamlit as st

def generate_report(rows):
    if not rows:
        st.info("No data available for report.")
        return
    
    # Convert data into DataFrame
    df = pd.DataFrame([dict(row._mapping) for row in rows])

    # Show table
    st.subheader(" Data Preview")
    st.dataframe(df)

    # Chart
    st.subheader("Chart")

    numeric_cols = df.select_dtypes(include=['number']).columns
    category_cols = df.select_dtypes(exclude=['number']).columns

    if len(numeric_cols) > 0 and len(category_cols) > 0:
        chart_df = df[[category_cols[0], numeric_cols[0]]].set_index(category_cols[0])
        st.bar_chart(chart_df)
    else:
        st.info("Not enough data for visualization")

    # Download
    st.download_button(
        label= "Download CSV",
        data=df.to_csv(index=False),
        file_name="report.csv",
        mime="text/csv"
    )