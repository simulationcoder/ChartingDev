import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import math

# Function to calculate the price of a European call or put option using the Black-Scholes model
def black_scholes_option_price(S, K, T, r, sigma, option_type="call"):
    """
    Calculate the Black-Scholes price for a European call or put option.
    """
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)

    if option_type == "call":
        price = (S * norm.cdf(d1)) - (K * math.exp(-r * T) * norm.cdf(d2))
    else:  # put option
        price = (K * math.exp(-r * T) * norm.cdf(-d2)) - (S * norm.cdf(-d1))

    return price

# Function to plot the payoff diagram
def plot_payoff_diagram(S, K, premium, option_type="call"):
    """
    Plot the payoff diagram for a European call or put option.
    """
    if option_type == "call":
        payoff = np.maximum(S - K, 0) - premium
    else:  # put option
        payoff = np.maximum(K - S, 0) - premium

    # Plotting the payoff diagram
    plt.figure(figsize=(10, 6))
    plt.plot(S, payoff, label=f'{option_type.capitalize()} Option Payoff', color='blue')
    plt.axhline(0, color='black', linestyle='--', linewidth=1)
    plt.axvline(K, color='red', linestyle='--', label='Strike Price')
    plt.fill_between(S, 0, payoff, where=(payoff > 0), color='blue', alpha=0.2)
    plt.title(f"{option_type.capitalize()} Option Payoff Diagram")
    plt.xlabel("Stock Price at Expiration")
    plt.ylabel("Profit / Loss")
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)

# Streamlit Web App
st.markdown(
    """
    <h2 style='text-align: center; color: #007ACC; font-size: 26px;'>
    European Option Pricing and Payoff Diagram using Black-Sholes Formula
    </h2>
    """,
    unsafe_allow_html=True
)
# Create a 3-row, 2-column layout
col1, col2 = st.columns(2)

# First row inputs
with col1:
    S = st.number_input("Current Stock Price (S)", value=100.0, min_value=0.0, step=1.0)
with col2:
    K = st.number_input("Strike Price (K)", value=100.0, min_value=0.0, step=1.0)

# Second row inputs
with col1:
    T = st.number_input("Time to Maturity (T in years)", value=1.0, min_value=0.01, step=0.01)
with col2:
    r = st.number_input("Risk-Free Interest Rate (r)", value=0.05, min_value=0.0, step=0.01)

# Third row inputs
with col1:
    sigma = st.number_input("Volatility (σ)", value=0.2, min_value=0.01, step=0.01)
with col2:
    option_type = st.selectbox("Option Type", options=["call", "put"])

# Calculate option price
option_price = black_scholes_option_price(S, K, T, r, sigma, option_type)
st.write(f"The European {option_type} option price is: ${option_price:.2f}")

# Plot the payoff diagram
premium = option_price
stock_prices = np.linspace(0.5 * S, 1.5 * S, 500)
plot_payoff_diagram(stock_prices, K, premium, option_type)