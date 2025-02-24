import pandas as pd

def process_sheet(input_path, output_path, config):
    # Read the input sheet
    df = pd.read_excel(input_path, dtype=str)  # Read all columns as strings to avoid type issues

    # Define standardized column names in the required order
    columns = ["ISBN", "Title", "Price", "Stock", "Publisher", "Threshold"]

    # Initialize a dictionary to store extracted data
    master_data = {col: [] for col in columns}

    # Function to get a column based on config, handling missing cases
    def get_column(df, key):
        col_index = config.get(key)
        if col_index is not None:
            col_index -= 1  # Convert 1-based to 0-based indexing
            if col_index >= 0 and col_index < len(df.columns):
                return df.iloc[:, col_index].fillna("").tolist()
        return [""] * len(df)  # Return empty values if column is missing

    # Identify the column dynamically for "Stock"
    stock_column_names = ["Stock", "Qty", "BDSStock", "Available Stock", "ClosingStock", "Stock Status", "Remarks", "Stock Position", "SOH", "Total", "In Stock>10", "Zoho Stock", "HO", "Availability Status", "BQ", "AllTotal", "SRT"]
    
    def find_stock_column(df):
        for col_name in stock_column_names:
            for actual_col in df.columns:
                if col_name.lower() in actual_col.lower():
                    return df[actual_col].fillna("").tolist()
        return [""] * len(df)  # Default to empty if no match is found

    # Extract data using column mapping from config
    master_data["ISBN"] = get_column(df, "ISBN")
    master_data["Title"] = get_column(df, "Title")
    master_data["Price"] = get_column(df, "Price")
    master_data["Stock"] = find_stock_column(df)  # Dynamically find Stock column

    # Assign Publisher name (fixed value, not from sheet)
    master_data["Publisher"] = get_column(df, "Publisher")

    # Set a default Threshold value
    master_data["Threshold"] = ["10"] * len(df)  # Default threshold set to 10

    # Create DataFrame with correct column order
    master_df = pd.DataFrame(master_data, columns=columns)

    # Save the formatted data to an Excel file
    master_df.to_excel(output_path, index=False)

    print(f"Processed sheet saved to {output_path}")
