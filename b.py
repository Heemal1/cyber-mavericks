import streamlit as st
import pandas as pd
import plotly.express as px

# App Title
st.title("Multi-File EDA - Combine and Analyze")

# File Upload Section
uploaded_files = st.file_uploader("Upload multiple Excel files (.xlsx or .xls)", type=["xlsx", "xls"], accept_multiple_files=True)

if uploaded_files:
    try:
        # Load and merge data from multiple files
        dfs = []
        for file in uploaded_files:
            df = pd.read_excel(file)
            dfs.append(df)

        # Combine all files into one DataFrame
        combined_df = pd.concat(dfs, ignore_index=True)

        # Display the first few rows of the merged data
        st.header("Combined Data Preview")
        st.dataframe(combined_df.head())

        # Display basic information about the merged dataset
        st.header("Combined Dataset Information")
        st.write(f"**Number of Rows:** {combined_df.shape[0]}")
        st.write(f"**Number of Columns:** {combined_df.shape[1]}")
        st.write("**Columns and Data Types:**")
        st.write(combined_df.dtypes)

        # Display summary statistics
        st.header("Summary Statistics")
        st.write(combined_df.describe())

        # Show missing values in the dataset
        st.header("Missing Values")
        st.write(combined_df.isnull().sum())

        # Column selection for visualizations
        st.header("Visualizations")
        numeric_columns = combined_df.select_dtypes(include=["number"]).columns.tolist()
        categorical_columns = combined_df.select_dtypes(include=["object"]).columns.tolist()

        # Histogram for numeric columns
        st.subheader("Histogram (Numeric Columns)")
        selected_numeric_col = st.selectbox("Select a numeric column for histogram:", numeric_columns)
        if selected_numeric_col:
            fig = px.histogram(combined_df, x=selected_numeric_col, title=f"Distribution of {selected_numeric_col}")
            st.plotly_chart(fig)

        # Bar chart for categorical columns
        st.subheader("Bar Chart (Categorical Columns)")
        selected_categorical_col = st.selectbox("Select a categorical column for bar chart:", categorical_columns)
        if selected_categorical_col:
            # Prepare data for Plotly
            categorical_data = combined_df[selected_categorical_col].value_counts().reset_index()
            categorical_data.columns = [selected_categorical_col, "count"]

            fig = px.bar(
                categorical_data,
                x=selected_categorical_col, 
                y="count", 
                title=f"Bar Chart for {selected_categorical_col}",
                labels={selected_categorical_col: "Category", "count": "Frequency"}
            )
            st.plotly_chart(fig)

        # Scatter plot for relationships between numeric columns
        st.subheader("Scatter Plot (Numeric Columns)")
        x_axis = st.selectbox("Select the X-axis (numeric):", numeric_columns)
        y_axis = st.selectbox("Select the Y-axis (numeric):", numeric_columns)
        if x_axis and y_axis:
            fig = px.scatter(combined_df, x=x_axis, y=y_axis, title=f"Scatter Plot: {x_axis} vs {y_axis}")
            st.plotly_chart(fig)

    except Exception as e:
        st.error(f"Error processing files: {str(e)}")