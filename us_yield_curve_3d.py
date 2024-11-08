import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Load the dataset
df = pd.read_csv("files/yieldCurve.csv")  # Replace with your actual file path

# Convert the 'Date' column to datetime format
df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')

# Convert the yield columns (1M, 2M, 3M, ..., 30Y) to numeric, forcing errors to NaN
tenors = df.columns[1:]  # Extract tenor columns (1M, 2M, 3M, ..., 30Y)
df[tenors] = df[tenors].apply(pd.to_numeric, errors='coerce')

# Drop rows with NaN values in the yield columns
df = df.dropna(subset=tenors)

# Prepare the data for plotting
dates = df['Date'].values  # Date values
tenor_labels = [tenor for tenor in tenors]  # Keep full tenor labels (e.g., '1M', '2M', etc.)

# Convert dates to number of days since the first date
date_min = min(dates)  # Find the earliest date
Y = (dates - date_min).astype('timedelta64[D]').astype(int)  # Convert to number of days

# Convert tenor labels to numeric values (1M -> 1, 2M -> 2, etc.)
tenor_values = [int(tenor[:-1]) if tenor[-1] != 'Y' else int(tenor[:-1]) * 12 for tenor in tenor_labels]
X = np.array(tenor_values)  # Numeric values for tenors

# Create a meshgrid for the 3D plot
Y_grid, X_grid = np.meshgrid(Y, X)
print(Y_grid)
print(X_grid)

# Prepare the Z data (Yield rates)
# Reshape the Z data to match the shape of the meshgrid
Z = df[tenors].values.T  # Transpose to match shape (tenors x dates)

# Create the 3D plot
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Plot the surface with the 'viridis' colormap
ax.plot_surface(X_grid, Y_grid, Z, cmap='plasma')

# Set labels
ax.set_xlabel('Tenor (1M -30 Years)')
ax.set_ylabel('Date - converted into x(th) day of the year')
ax.set_zlabel('Yield Rate (%)')
ax.set_title('US Yield Curve (Data for Tenors [1 month - 30 Years ]) for 2024')

# Show the plot
plt.show()