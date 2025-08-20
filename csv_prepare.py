import pandas as pd
import os

file_write = True      # True for write
mt5_forex_tester5_format = True     # Prepare CSV for Forex Tester 5 / BCS_1 / GU_GT_RECOGNITION
tc2000_format = False
mt4_format = False  # False for MT5 format
file_path = 'MNQU25_M30.csv'

# Extract the original file name without extension
original_name = os.path.splitext(os.path.basename(file_path))[0]

# Append symbols or text to the original name
new_filename = f"{original_name}_modified.csv"

# Read the CSV file
df = pd.read_csv(file_path, parse_dates=[0], delimiter='\t')  # Tab is default delimiter for MT5 files

# Delete the last two columns
df = df.drop(df.columns[-2:], axis=1)


# Define new column names based on the specified format
new_column_names = {
        '<DATE>': 'Date',
        '<TIME>': 'Time',
        '<OPEN>': 'Open',
        '<HIGH>': 'High',
        '<LOW>': 'Low',
        '<CLOSE>': 'Close',
        '<TICKVOL>': 'Volume'
    }
# Rename columns based on the specified format
df = df.rename(columns=new_column_names)

# Convert 'Date' and 'Time' to a single 'Datetime' column
df['Datetime'] = pd.to_datetime(df['Date'].astype(str) + ' ' + df['Time'])

# Place 'Datetime' at the beginning of the DataFrame
df = df[['Datetime'] + [col for col in df.columns if col != 'Datetime']]

# Delete the original 'Date' and 'Time' columns
df = df.drop(columns=['Date', 'Time'])

print(df)
# Save the modified CSV
if file_write:
    df.to_csv(new_filename, index=False, sep=',')
    print(f"File saved as: {new_filename}")
else:
    pass
