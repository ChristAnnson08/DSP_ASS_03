import pandas as pd
import altair as alt

class NumericColumn:
    """
    Class to analyze a numeric column in a DataFrame.
    """

    def __init__(self, file_path=None, df=None):
        self.file_path = file_path
        self.df = df
        self.cols_list = []
        self.serie = None
        self.n_unique = None
        self.n_missing = None
        self.col_mean = None
        self.col_std = None
        self.col_min = None
        self.col_max = None
        self.col_median = None
        self.n_zeros = None
        self.n_negatives = None
        self.histogram = alt.Chart()
        self.frequent = pd.DataFrame(columns=['value', 'occurrence', 'percentage'])

    def find_num_cols(self):
        """Find numeric columns in the dataset."""
        if self.df is None:
            self.df = pd.read_csv(self.file_path)
        self.cols_list = self.df.select_dtypes(include=['number']).columns.tolist()

    def set_data(self, col_name):
        """Set data for analysis by selecting a column and computing stats."""
        self.serie = self.df[col_name]
        self.convert_serie_to_num()
        self.is_serie_none()
        self.set_unique()
        self.set_missing()
        self.set_zeros()
        self.set_negatives()
        self.set_mean()
        self.set_std()
        self.set_min()
        self.set_max()
        self.set_median()
        self.set_histogram()
        self.set_frequent()

    def convert_serie_to_num(self):
        """Convert the column to numeric, handling errors."""
        self.serie = pd.to_numeric(self.serie, errors='coerce')

    def is_serie_none(self):
        """Check if the series is empty or None."""
        return self.serie is None or self.serie.empty

    def set_unique(self):
        """Count unique values in the series."""
        if not self.is_serie_none():
            self.n_unique = self.serie.nunique()

    def set_missing(self):
        """Count missing values in the series."""
        if not self.is_serie_none():
            self.n_missing = self.serie.isnull().sum()

    def set_zeros(self):
        """Count occurrences of 0 in the series."""
        if not self.is_serie_none():
            self.n_zeros = (self.serie == 0).sum()

    def set_negatives(self):
        """Count negative values in the series."""
        if not self.is_serie_none():
            self.n_negatives = (self.serie < 0).sum()

    def set_mean(self):
        """Calculate the mean of the series."""
        if not self.is_serie_none():
            self.col_mean = self.serie.mean()

    def set_std(self):
        """Calculate the standard deviation of the series."""
        if not self.is_serie_none():
            self.col_std = self.serie.std()

    def set_min(self):
        """Find the minimum value of the series."""
        if not self.is_serie_none():
            self.col_min = self.serie.min()

    def set_max(self):
        """Find the maximum value of the series."""
        if not self.is_serie_none():
            self.col_max = self.serie.max()

    def set_median(self):
        """Find the median value of the series."""
        if not self.is_serie_none():
            self.col_median = self.serie.median()

    def set_histogram(self):
        """Create a histogram for the series values."""
        if not self.is_serie_none():
            chart = alt.Chart(self.serie.reset_index()).mark_bar().encode(
                alt.X(f"{self.serie.name}:O", title="Values", sort=alt.EncodingSortField(field="count", order="descending")),
                alt.Y("count():Q", title="Count")
            ).properties(title=f"Histogram Plot: Distribution of Values in {self.serie.name}")
            self.histogram = chart

    def set_frequent(self, end=20):
        """Get the most frequent values in the series."""
        if not self.is_serie_none():
            frequent_values = self.serie.value_counts().head(end).reset_index()
            frequent_values.columns = ['value', 'occurrence']
            frequent_values['percentage'] = (
                (frequent_values['occurrence'] / len(self.serie)) * 100
            ).round(2).astype(str)

            self.frequent = frequent_values

    def get_summary(self):
        """Generate a summary of the series statistics."""
        summary_df = pd.DataFrame({
            'Description': [
                'Number of Unique Values', 
                'Number of Missing Values', 
                'Number of Occurrences of 0',  
                'Number of Negative Values',  
                'Average Value',  
                'Standard Deviation',    
                'Minimum Value',  
                'Maximum Value', 
                'Median Value'
            ],
            'Value': [
                self.n_unique, 
                self.n_missing, 
                self.n_zeros, 
                self.n_negatives, 
                self.col_mean, 
                self.col_std, 
                self.col_min, 
                self.col_max, 
                self.col_median
            ]
        })
        return summary_df
