import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Directory where your CSV files are stored
directory = "files"  # Change to your actual directory path

# Get all CSV filenames in the directory
csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]

# Create a dropdown with the filenames
file_name = st.selectbox("Select a file", csv_files)

# Load the selected CSV file
file_path = os.path.join(directory, file_name)
data = pd.read_csv(file_path)

# Convert the 'Date' column to datetime
data['Date'] = pd.to_datetime(data['Date'])

# Plot Date vs Close
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(data['Date'], data['Close'], label='Close', color='blue')

# Add labels and title
ax.set_xlabel('Date')
ax.set_ylabel('Close Price')
ax.set_title(f"Date vs Close Price for {file_name}")

# Display the plot in Streamlit
st.pyplot(fig)