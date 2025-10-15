from imports import *
from data_cleaning import clean_data
from feature_engineering import engineer_features

class DataPipeline:
    """Combines data cleaning and feature engineering into a single pipeline."""

    def __init__(self, cleaning_fn=clean_data, feature_fn=engineer_features):
        self.cleaning_fn = cleaning_fn
        self.feature_fn = feature_fn

    def run(self, df: pd.DataFrame) -> pd.DataFrame:
        print("🔹 Starting data cleaning...")
        df_clean = self.cleaning_fn(df)
        print(f"✅ Cleaning complete. Shape: {df_clean.shape}")

        print("🔹 Starting feature engineering...")
        df_features = self.feature_fn(df_clean)
        print(f"✅ Feature engineering complete. Shape: {df_features.shape}")

        return df_features
