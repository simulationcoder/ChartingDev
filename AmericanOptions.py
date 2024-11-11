import numpy as np
import matplotlib.pyplot as plt

# Parameters
S0 = 100        # Initial stock price
K = 100         # Strike price
T = 1.0         # Time to maturity (in years)
r = 0.05        # Risk-free rate
sigma = 0.2     # Volatility
N = 10000       # Number of Monte Carlo simulations
M = 50          # Number of time steps

np.random.seed(42)

# Step 1: Generate Monte Carlo paths
dt = T / M
discount_factor = np.exp(-r * dt)

# Initialize stock price paths
S = np.zeros((N, M + 1))
S[:, 0] = S0

# Simulate price paths
for t in range(1, M + 1):
    Z = np.random.standard_normal(N)
    S[:, t] = S[:, t-1] * np.exp((r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z)

# Step 2: Backward induction using Least Squares Monte Carlo
cash_flows = np.maximum(K - S[:, -1], 0)  # Payoff at maturity

# Loop backward in time to calculate the option value
for t in range(M-1, 0, -1):
    # Select paths where the option is in the money
    in_the_money = np.where(K > S[:, t])[0]
    
    # If no paths are in the money, continue
    if len(in_the_money) == 0:
        continue
    
    # Regression on in-the-money paths
    X = S[in_the_money, t]
    Y = cash_flows[in_the_money] * discount_factor
    
    # Fit a polynomial regression (e.g., quadratic) to estimate continuation value
    A = np.vstack([np.ones_like(X), X, X**2]).T
    coeffs = np.linalg.lstsq(A, Y, rcond=None)[0]
    continuation_value = coeffs[0] + coeffs[1] * X + coeffs[2] * X**2

    # Calculate immediate exercise value
    exercise_value = K - X
    
    # Determine which paths to exercise
    exercise = exercise_value > continuation_value
    cash_flows[in_the_money[exercise]] = exercise_value[exercise]
    cash_flows *= discount_factor

# Step 3: Calculate the option price
option_price = np.mean(cash_flows) * np.exp(-r * dt)
print(f"American Put Option Price: {option_price:.2f}")

# Plot some simulated paths
plt.figure(figsize=(10, 6))
plt.plot(S[:5].T)
plt.title("Simulated Stock Price Paths")
plt.xlabel("Time Steps")
plt.ylabel("Stock Price")
plt.grid(True)
plt.show()