import pandas as pd
import altair as alt

class DateColumn:
    def __init__(self, file_path=None, df=None):
        self.file_path = file_path
        self.df = pd.read_csv(file_path) if file_path else df
        self.cols_list = []
        self.serie = None
        self.summary_data = {}
        self.barchart = None
        self.frequent = pd.DataFrame(columns=['value', 'occurrence', 'percentage'])

    def find_date_cols(self):
        if self.df is not None:
            date_cols = self.df.select_dtypes(include=['datetime64']).columns.tolist()
            if not date_cols:
                object_columns = self.df.select_dtypes(include=['object'])
                self.cols_list = [col for col in object_columns.columns if pd.to_datetime(self.df[col], errors='coerce').notnull().any()]
            else:
                self.cols_list = date_cols

    def set_data(self, col_name):
        if col_name in self.df.columns:
            self.serie = pd.to_datetime(self.df[col_name], errors='coerce')
            self._calculate_summary()
            self._generate_barchart()
            self._calculate_frequent_values()
        else:
            raise ValueError(f"Column '{col_name}' not found in the DataFrame.")

    def _calculate_summary(self):
        # Setting the order of the descriptions as per the display in the screenshot
        self.summary_data = {
            "Number of Unique Values": self.serie.nunique(),
            "Number of Rows with Missing Values": self.serie.isna().sum(),
            "Number of Weekend Dates": self.serie.dt.dayofweek.isin([5, 6]).sum(),
            "Number of Weekday Dates": (~self.serie.dt.dayofweek.isin([5, 6])).sum(),
            "Number of Dates in Future": (self.serie > pd.Timestamp.now()).sum(),
            "Number of Rows with 1900-01-01": (self.serie == pd.Timestamp("1900-01-01")).sum(),
            "Number of Rows with 1970-01-01": (self.serie == pd.Timestamp("1970-01-01")).sum(),
            "Minimum Value": self.serie.min(),
            "Maximum Value": self.serie.max()
        }

    def _generate_barchart(self):
        year_counts = self.serie.dt.year.value_counts().reset_index()
        year_counts.columns = ['year', 'count']
        self.barchart = alt.Chart(year_counts).mark_bar().encode(
            x=alt.X('year:T', title='Year'),
            y=alt.Y('count:Q', title='Count of Records')
        )

    def _calculate_frequent_values(self, end=20):
        counts = self.serie.value_counts().head(end)
        self.frequent = pd.DataFrame({
            'value': counts.index,
            'occurrence': counts.values,
            'percentage': (counts / counts.sum()).round(4)
        })

    def get_summary(self):
        # Creating a DataFrame from the summary dictionary in the specified order
        ordered_summary = [
            "Number of Unique Values",
            "Number of Rows with Missing Values",
            "Number of Weekend Dates",
            "Number of Weekday Dates",
            "Number of Dates in Future",
            "Number of Rows with 1900-01-01",
            "Number of Rows with 1970-01-01",
            "Minimum Value",
            "Maximum Value"
        ]
        summary_df = pd.DataFrame(
            [(desc, self.summary_data[desc]) for desc in ordered_summary],
            columns=["Description", "Value"]
        )
        return summary_df
