import pandas as pd
import numpy as np

class DataAnalyzer:
    def __init__(self):
        self.df = None
        self.cleaned_df = None

    def load_data(self, file_path):
        try:
            self.df = pd.read_csv(file_path)
            # Ensure Date column is datetime
            if "Date" in self.df.columns:
                self.df["Date"] = pd.to_datetime(self.df["Date"])
            return True, "Data loaded successfully"
        except Exception as e:
            return False, f"Error loading data: {str(e)}"

    def preprocess_data(self):
        if self.df is None:
            return False, "No data loaded"
        
        # 1. Handle missing values
        # For numeric columns, fill with median
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        self.df[numeric_cols] = self.df[numeric_cols].fillna(self.df[numeric_cols].median())
        
        # For categorical columns, fill with mode or 'Unknown'
        categorical_cols = self.df.select_dtypes(exclude=[np.number]).columns
        for col in categorical_cols:
            self.df[col] = self.df[col].fillna(self.df[col].mode()[0] if not self.df[col].mode().empty else "Unknown")
            
        # 2. Remove duplicates
        initial_count = len(self.df)
        self.df = self.df.drop_duplicates()
        removed_duplicates = initial_count - len(self.df)
        
        self.cleaned_df = self.df.copy()
        return True, f"Preprocessing complete. Removed {removed_duplicates} duplicates. Missing values handled."

    def get_summary_stats(self):
        if self.cleaned_df is None:
            return None
        
        stats = {
            "Total Sales": self.cleaned_df["Total_Amount"].sum(),
            "Total Transactions": len(self.cleaned_df),
            "Avg Transaction Value": self.cleaned_df["Total_Amount"].mean(),
            "Top Product": self.cleaned_df.groupby("Product")["Total_Amount"].sum().idxmax(),
            "Total Customers": self.cleaned_df["Customer_ID"].nunique()
        }
        return stats

    def get_top_customers(self, n=5):
        if self.cleaned_df is None: return None
        return self.cleaned_df.groupby("Customer_ID")["Total_Amount"].sum().sort_values(ascending=False).head(n)

    def get_product_performance(self):
        if self.cleaned_df is None: return None
        return self.cleaned_df.groupby("Product")["Total_Amount"].sum().sort_values(ascending=False)

    def get_sales_trends(self):
        if self.cleaned_df is None: return None
        # Group by month
        trends = self.cleaned_df.copy()
        trends["Month"] = trends["Date"].dt.to_period("M")
        return trends.groupby("Month")["Total_Amount"].sum()

    def get_regional_distribution(self):
        if self.cleaned_df is None: return None
        return self.cleaned_df.groupby("Region")["Total_Amount"].sum()
