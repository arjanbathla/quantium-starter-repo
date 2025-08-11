import pandas as pd
import os

def process_soul_foods_data():
    """
    Process Soul Foods CSV files to extract pink morsel data and calculate sales.
    Output will contain: Sales, Date, Region
    """
    
    # List of CSV files to process
    csv_files = [
        'data/daily_sales_data_0.csv',
        'data/daily_sales_data_1.csv', 
        'data/daily_sales_data_2.csv'
    ]
    
    # List to store processed dataframes
    processed_dfs = []
    
    for file_path in csv_files:
        if os.path.exists(file_path):
            print(f"Processing {file_path}...")
            
            # Read CSV file
            df = pd.read_csv(file_path)
            
            # Filter for pink morsels only (case insensitive)
            pink_morsels = df[df['product'].str.lower() == 'pink morsel'].copy()
            
            if len(pink_morsels) > 0:
                # Clean price column by removing '$' and converting to float
                pink_morsels['price'] = pink_morsels['price'].str.replace('$', '').astype(float)
                
                # Calculate sales (price * quantity)
                pink_morsels['sales'] = pink_morsels['price'] * pink_morsels['quantity']
                
                # Select only the required columns and rename for clarity
                processed_df = pink_morsels[['sales', 'date', 'region']].copy()
                
                processed_dfs.append(processed_df)
                print(f"  - Found {len(pink_morsels)} pink morsel records")
            else:
                print(f"  - No pink morsel records found in {file_path}")
        else:
            print(f"Warning: File {file_path} not found")
    
    if processed_dfs:
        # Combine all processed dataframes
        combined_df = pd.concat(processed_dfs, ignore_index=True)
        
        # Sort by date and region for better organization
        combined_df = combined_df.sort_values(['date', 'region'])
        
        # Save to output file
        output_file = 'soul_foods_pink_morsels_sales.csv'
        combined_df.to_csv(output_file, index=False)
        
        print(f"\nProcessing complete!")
        print(f"Total records: {len(combined_df)}")
        print(f"Output saved to: {output_file}")
        
        # Display sample of the output
        print(f"\nSample of processed data:")
        print(combined_df.head(10))
        
        # Display summary statistics
        print(f"\nSummary by region:")
        print(combined_df.groupby('region')['sales'].agg(['count', 'sum', 'mean']).round(2))
        
        return combined_df
    else:
        print("No data was processed. Please check the input files.")
        return None

if __name__ == "__main__":
    process_soul_foods_data() 