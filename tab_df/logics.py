import pandas as pd

class Dataset:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None
        self.cols_list = []
        self.n_rows = 0
        self.n_cols = 0
        self.n_duplicates = 0
        self.n_missing = 0
        self.n_num_cols = 0
        self.n_text_cols = 0
        self.table = None

    def load_data(self):
        self.load_df()
        if not self.is_df_empty():
            self.extract_columns()
            self.calculate_dimensions()
            self.find_duplicates()
            self.find_missing()
            self.identify_numeric()
            self.identify_text()
            self.create_summary_table()

    def load_df(self):
        if self.df is None:
            self.df = pd.read_csv(self.file_path)

    def is_df_empty(self):
        return self.df is None

    def extract_columns(self):
        if not self.is_df_empty():
            self.cols_list = self.df.columns.tolist()

    def calculate_dimensions(self):
        if not self.is_df_empty():
            self.n_rows, self.n_cols = self.df.shape

    def find_duplicates(self):
        if not self.is_df_empty():
            self.n_duplicates = self.df.duplicated().sum()

    def find_missing(self):
        if not self.is_df_empty():
            self.n_missing = self.df.isnull().sum().sum()

    def identify_numeric(self):
        if not self.is_df_empty():
            self.n_num_cols = len(self.df.select_dtypes(include=['number']).columns)

    def identify_text(self):
        if not self.is_df_empty():
            self.n_text_cols = len(self.df.select_dtypes(include=['object']).columns)

    def show_head(self, n=5):
        if not self.is_df_empty():
            return self.df.head(n)

    def show_tail(self, n=5):
        if not self.is_df_empty():
            return self.df.tail(n)

    def show_sample(self, n=5):
        if not self.is_df_empty():
            return self.df.sample(n)

    def create_summary_table(self):
        if not self.is_df_empty():
            col_info = []
            for col in self.df.columns:
                col_info.append({
                    'Column Name': col,
                    'Data Type': str(self.df[col].dtype),
                    'Memory Usage (KB)': round(self.df[col].memory_usage(deep=True) / 1024, 2)
                })
            self.table = pd.DataFrame(col_info)

    def generate_summary(self):
        summary = {
            'Description': [
                'Number of Rows', 
                'Number of Columns', 
                'Number of Duplicated Rows', 
                'Number of Rows with Missing Values'
            ],
            'Value': [
                self.n_rows, 
                self.n_cols, 
                self.n_duplicates, 
                self.n_missing
            ]
        }
        summary_df = pd.DataFrame(summary)
        return summary_df
