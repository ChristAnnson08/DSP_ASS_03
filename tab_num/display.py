import streamlit as st

from tab_num.logics import NumericColumn

def display_tab_num_content(file_path=None, df=None):
    """
    --------------------
    Description
    --------------------
    -> display_tab_num_content (function): Function that will instantiate tab_num.logics.NumericColumn class, save it into Streamlit session state and call its tab_num.logics.NumericColumn.find_num_cols() method in order to find all numeric columns.
    Then it will display a Streamlit select box with the list of numeric columns found.
    Once the user select a numeric column from the select box, it will call the tab_num.logics.NumericColumn.set_data() method in order to compute all the information to be displayed.
    Then it will display a Streamlit Expander container with the following contents:
    - the results of tab_num.logics.NumericColumn.get_summary() as a Streamlit Table
    - the graph from tab_num.logics.NumericColumn.histogram using Streamlit.altair_chart()
    - the results of tab_num.logics.NumericColumn.frequent using Streamlit.write
 
    --------------------
    Parameters
    --------------------
    -> file_path (str): File path to uploaded CSV file (optional)
    -> df (pd.DataFrame): Loaded dataframe (optional)

    --------------------
    Returns
    --------------------
    -> None

    """

    if file_path or (df is not None):
        # Instantiate DateColumn in Streamlit session state
        if file_path:
            st.session_state.num_column = NumericColumn(file_path=file_path)
        else:
            st.session_state.num_column = NumericColumn(df=df)
            
    # Find datetime columns
    st.session_state.num_column.find_num_cols()

    # Display a Streamlit select box with the list of numeric columns found
    selected_numeric_column = st.selectbox("Select Numeric Column", st.session_state.num_column.cols_list)

    # Once the user selects a numeric column, compute and display the information
    if selected_numeric_column:
        st.session_state.num_column.set_data(selected_numeric_column)

        # Display results in a Streamlit Expander container
        with st.expander("Numeric Column Analysis"):
            # Display results of get_summary() as a Streamlit Table
            st.table(st.session_state.num_column.get_summary())

            # Display graph from histogram using Streamlit.altair_chart()
            st.altair_chart(st.session_state.num_column.histogram, use_container_width=True)

            # Display results of frequent using Streamlit.write
            st.write("Top 20 Most Frequent Values:")
            st.write(st.session_state.num_column.frequent)
