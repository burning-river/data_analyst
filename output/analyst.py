import pandas as pd
#from typing import tuple, dict, Union

class Analyst:
    def __init__(self) -> None:
        self.data = None

    def upload_csv(self, file_path: str) -> None:
        try:
            self.data = pd.read_csv(file_path)
        except FileNotFoundError:
            raise FileNotFoundError(f"The file at '{file_path}' was not found.")
        except pd.errors.EmptyDataError:
            raise ValueError(f"The file at '{file_path}' is empty.")
        except pd.errors.ParserError:
            raise ValueError(f"The file at '{file_path}' could not be parsed as CSV.")
        except Exception as e:
            raise RuntimeError(f"An error occurred while reading the file: {e}")

    def get_data_size(self):# -> tuple[int, int]:
        if self.data is None:
            raise ValueError("No data loaded. Please upload a CSV file first.")
        return self.data.shape

    def get_column_data_types(self):# -> dict[str, str]:
        if self.data is None:
            raise ValueError("No data loaded. Please upload a CSV file first.")
        # pandas dtype names are already strings like 'int64', 'float64', 'object'
        return self.data.dtypes.apply(lambda dt: dt.name).to_dict()

    def get_missing_values_count(self):# -> dict[str, int]:
        if self.data is None:
            raise ValueError("No data loaded. Please upload a CSV file first.")
        return self.data.isnull().mean().to_dict()

    def get_numeric_column_stats(self): #-> dict[str, dict[str, float]]:
        if self.data is None:
            raise ValueError("No data loaded. Please upload a CSV file first.")
        numeric_stats = {}
        numeric_cols = self.data.select_dtypes(include=['number']).columns
        for col in numeric_cols:
            col_data = self.data[col].dropna()
            if col_data.empty:
                # If all values are missing, stats are not available
                numeric_stats[col] = {
                    "mean": float('nan'),
                    "median": float('nan'),
                    "mode": float('nan'),
                    "std_dev": float('nan'),
                    "range": float('nan')
                }
                continue
            mean_val = col_data.mean()
            median_val = col_data.median()
            modes = col_data.mode()
            mode_val = modes.iloc[0] if not modes.empty else float('nan')
            std_dev_val = col_data.std(ddof=0)  # population std deviation (ddof=0)
            range_val = col_data.max() - col_data.min()
            numeric_stats[col] = {
                "mean": float(mean_val),
                "median": float(median_val),
                "mode": float(mode_val),
                "std_dev": float(std_dev_val),
                "range": float(range_val)
            }
        return numeric_stats

    def get_categorical_column_stats(self):# -> dict[str, dict[str, Union[int, str]]]:
        if self.data is None:
            raise ValueError("No data loaded. Please upload a CSV file first.")
        categorical_stats = {}
        # Categorical columns are those with dtype 'object' or categorical or bool
        cat_cols = self.data.select_dtypes(include=['object', 'category', 'bool']).columns
        for col in cat_cols:
            col_data = self.data[col].dropna()
            if col_data.empty:
                mode_val = None
                unique_count = 0
            else:
                modes = col_data.mode()
                mode_val = modes.iloc[0] if not modes.empty else None
                unique_count = col_data.nunique()
            categorical_stats[col] = {
                "mode": mode_val,
                "unique_values": unique_count
            }
        return categorical_stats
