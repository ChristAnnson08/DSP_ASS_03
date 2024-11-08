import pandas as pd
import altair as alt

class TextColumn:
    def __init__(self, file_path=None, df=None):
        self.file_path = file_path
        self.df = df
        self.cols_list = []
        self.serie = None
        self.n_unique = None
        self.n_missing = None
        self.n_empty = None
        self.n_mode = None
        self.n_space = None
        self.n_lower = None
        self.n_upper = None
        self.n_alpha = None
        self.n_digit = None
        self.barchart = alt.Chart()
        self.frequent = pd.DataFrame(columns=['value', 'occurrence', 'percentage'])

    def find_text_cols(self):
        if self.df is None:
            self.df = pd.read_csv(self.file_path)

        self.cols_list = [col for col in self.df.columns if self.df[col].dtype == 'object']

    def set_data(self, col_name):
        self.serie = self.df[col_name]
        self.convert_serie_to_text()
        self.set_unique()
        self.set_missing()
        self.set_empty()
        self.set_mode()
        self.set_whitespace()
        self.set_lowercase()
        self.set_uppercase()
        self.set_alphabet()
        self.set_digit()
        self.set_barchart()
        self.set_frequent()

    def convert_serie_to_text(self):
        self.serie = self.serie.astype(str)

    def is_serie_none(self):
        return self.serie is None

    def set_unique(self):
        self.n_unique = len(self.serie.unique())

    def set_missing(self):
        self.n_missing = self.serie.isnull().sum()

    def set_empty(self):
        self.n_empty = (self.serie == '').sum()

    def set_mode(self):
        self.n_mode = self.serie.mode().iloc[0]

    def set_whitespace(self):
        self.n_space = (self.serie == ' ').sum()

    def set_lowercase(self):
        self.n_lower = self.serie.str.islower().sum()

    def set_uppercase(self):
        self.n_upper = self.serie.str.isupper().sum()

    def set_alphabet(self):
        self.n_alpha = self.serie.str.isalpha().sum()

    def set_digit(self):
        self.n_digit = self.serie.str.isdigit().sum()

    def set_barchart(self):
        if not self.is_serie_none():
            chart = alt.Chart(self.serie.reset_index()).mark_bar().encode(
                alt.X(f"{self.serie.name}:O", title="AGE_DESC", sort=alt.EncodingSortField(field="count", order="descending")),
                alt.Y("count():Q", title="Count of Records")
            ).properties(title=" Chart")

            self.barchart = chart
            
    def set_frequent(self, end=20):
        if not self.is_serie_none():
            frequent_values = self.serie.value_counts().head(end).reset_index()
            frequent_values.columns = ['value', 'occurrence']
            frequent_values['percentage'] = (
                frequent_values['occurrence'] / len(self.serie)
            ).round(4)

            self.frequent = frequent_values

    def get_summary(self):
        summary_df = pd.DataFrame({
            'Description': [
                'Number of Unique Values', 'Number of Rows with Missing Values', 'Number of Empty Rows',
                'Number of Rows with Only Whitespace', 'Number of Rows with Only Lowercases',
                'Number of Rows with Only Uppercases', 'Number of Rows with Only Alphabet',
                'Number of Rows with Only Digits', 'Mode Value'
            ],
            'Value': [
                self.n_unique, self.n_missing, self.n_empty, self.n_space, 
                self.n_lower, self.n_upper, self.n_alpha, self.n_digit, self.n_mode
            ]
        })
        summary_df["Value"] = summary_df["Value"].astype(str)
        return summary_df

    def get_frequent_values_table(self):
        return self.frequent
