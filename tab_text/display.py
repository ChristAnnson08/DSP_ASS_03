import streamlit as st
import altair as alt
from tab_text.logics import TextColumn

def display_tab_text_content(file_path=None, df=None):
    """
    --------------------
    Description
    --------------------
    This function displays information about text columns in a file or DataFrame. It creates an instance of the TextColumn class, which identifies text columns and calculates various metrics.

    Steps:
    1. Find all text columns and display them in a dropdown.
    2. When a text column is selected, calculate its metrics.
    3. Show:
       - Summary table of the selected column
       - Bar chart of value counts
       - Table of frequent values
    """
    
    # Create an instance of the TextColumn class
    if file_path or (df is not None):
        # Instantiate TextColumn in Streamlit session state
        if file_path:
            st.session_state.text_column = TextColumn(file_path=file_path)
        else:
            st.session_state.text_column = TextColumn(df=df)
            
    # Find all text columns
    st.session_state.text_column.find_text_cols()

    # Display a selection box for text columns
    selected_text_column = st.selectbox("Select Text Column", st.session_state.text_column.cols_list)

    # Set data for the selected text column
    st.session_state.text_column.set_data(selected_text_column)

    # Display an Expander container for the results
    with st.expander("Text Column Summary"):
        # Display summary table
        st.write("### Summary Table")
        st.table(st.session_state.text_column.get_summary())

        # Display bar chart
        st.write("### Bar Chart")
        st.altair_chart(st.session_state.text_column.barchart, use_container_width=True)

        # Display frequent values
        st.write("### Frequent Values")
        st.table(st.session_state.text_column.get_frequent_values_table())
