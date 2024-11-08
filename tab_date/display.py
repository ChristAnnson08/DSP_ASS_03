import streamlit as st
from tab_date.logics import DateColumn

def display_tab_date_content(file_path=None, df=None):
    """
    --------------------
    Description
    --------------------
    This function allows you to explore datetime columns in a CSV file or DataFrame. 
    It identifies datetime columns, displays a dropdown to select one, and then shows:
       - A summary table of the column's statistics
       - A bar chart of date occurrences by year
       - A table of the most frequent dates

    Parameters:
    - file_path (str): Optional file path to a CSV file.
    - df (pd.DataFrame): Optional loaded DataFrame.

    Returns:
    - None
    """
    
    # Instantiate DateColumn in Streamlit session state
    if file_path or (df is not None):
        if file_path:
            st.session_state.date_column = DateColumn(file_path=file_path)
        else:
            st.session_state.date_column = DateColumn(df=df)
            
    # Find datetime columns
    st.session_state.date_column.find_date_cols()
    
    # Create a select box to choose a datetime column
    selected_column = st.selectbox("Which datetime column do you want to explore?", st.session_state.date_column.cols_list)
    
    if selected_column:
        # Set data for the selected column
        st.session_state.date_column.set_data(selected_column)

        # Create an expander container to show information
        with st.expander("Date Column Summary"):
            # Display a summary table
            st.write("### Summary Table")
            summary = st.session_state.date_column.get_summary()
            st.table(summary)

            # Display a Bar Chart using Altair chart
            st.write("### Bar Chart")
            chart = st.session_state.date_column.barchart
            if chart is not None:
                st.altair_chart(chart, use_container_width=True)

            # Display the most frequent values
            st.write("### Most Frequent Values")
            frequent_values = st.session_state.date_column.frequent
            st.table(frequent_values)
