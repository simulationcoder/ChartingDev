import os
import pandas as pd
import archive.streamlit as st
import matplotlib.pyplot as plt

st.title("Nurral")

# Directory where your CSV files are stored
directory = "pricingData"
listings_file = os.path.join("files", "listings.csv")  # Path to your listings.csv

# Load the listings.csv file
listings_df = pd.read_csv(listings_file)

# Ensure the columns are named correctly
#listings_df.columns = ['ticker', 'name', 'exchange']
listings_df.columns = ['ticker','name','exchange','assetType','ipoDate','delistingDate','status','country']
# Get all CSV filenames in the directory
csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]

# Remove the '.csv' extension for display in the dropdown
csv_display_names = [os.path.splitext(f)[0] for f in csv_files]

# Create a dropdown with the filenames (without .csv)
selected_file = st.selectbox("Choose Ticker", csv_display_names)

# Map the display name back to the original filename with .csv
file_name = f"{selected_file}.csv"

# Get the associated name and exchange from listings.csv
selected_info = listings_df[listings_df['ticker'] == selected_file]

if not selected_info.empty:
    ticker_name = selected_info.iloc[0]['name']
    ticker_exchange = selected_info.iloc[0]['exchange']
    st.write(f"**Name**: {ticker_name}")
    st.write(f"**Exchange**: {ticker_exchange}")
else:
    st.write("No information available for the selected ticker.")

# Load the selected CSV file
file_path = os.path.join(directory, file_name)
data = pd.read_csv(file_path)

# Convert the 'Date' column to datetime
data['Date'] = pd.to_datetime(data['Date'])

# Add date inputs for selecting a date range
min_date = data['Date'].min()
max_date = data['Date'].max()

st.write(f"Date range available: {min_date.date()} to {max_date.date()}")

# Allow user to select start and end dates
start_date = st.date_input("Select start date", min_value=min_date, max_value=max_date, value=min_date)
end_date = st.date_input("Select end date", min_value=min_date, max_value=max_date, value=max_date)

# Filter the data based on the selected date range
filtered_data = data[(data['Date'] >= pd.Timestamp(start_date)) & (data['Date'] <= pd.Timestamp(end_date))]

# Plot Date vs Close for the filtered data
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(filtered_data['Date'], filtered_data['Close'], label='Close', color='blue')

# Add labels and title
ax.set_xlabel('Date')
ax.set_ylabel('Close Price')
ax.set_title(f"Date vs Close Price for {selected_file}")

# Display the plot in Streamlit
st.pyplot(fig)