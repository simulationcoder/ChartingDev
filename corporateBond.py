import pandas as pd
from workalendar.america import Canada
import matplotlib.pyplot as plt
from datetime import date

# Function to calculate bond cash flows
def calculate_bond_cashflows(issue_date, par_value, coupon_rate, maturity_years, freq='6M'):
    # Initialize calendar for business day adjustments in Canada
    calendar = Canada()

    # Determine the coupon payment schedule (semi-annual payments)
    coupon_payment_dates = []
    for i in range(1, maturity_years * 2 + 1):  # Semi-annual payments (2 per year)
        payment_date = issue_date + pd.DateOffset(months=6 * i)  # Payment every 6 months
        if calendar.is_holiday(payment_date):  # If the date is a holiday, adjust to next business day
            payment_date = calendar.add_business_days(payment_date, 1)
        coupon_payment_dates.append(payment_date)

    # Calculate the coupon payment amounts (5% of par value paid semi-annually)
    coupon_payment = par_value * coupon_rate / 2  # Semi-annual coupon

    # Cash flows: Coupons until maturity, then principal + last coupon
    cashflows = []
    for i, payment_date in enumerate(coupon_payment_dates):
        if i == len(coupon_payment_dates) - 1:
            # On the maturity date, add the principal + last coupon
            cashflows.append((payment_date, par_value + coupon_payment))
        else:
            cashflows.append((payment_date, coupon_payment))

    return cashflows

# Example parameters for the bond
#issue_date = pd.to_datetime("2024-11-08") # Issue date
#print(issue_date)
issue_date=pd.to_datetime(date.today())

par_value = 600000000  # Face value of the bond (par value, in CAD)
coupon_rate = 0.05  # Coupon rate of 5%
maturity_years = 5  # 5 years maturity

# Calculate the cash flows
cashflows = calculate_bond_cashflows(issue_date, par_value, coupon_rate, maturity_years)

# Extract dates and amounts from the cashflows
payment_dates = [cf[0] for cf in cashflows]
payment_amounts = [cf[1] for cf in cashflows]

# Print the results
for date, amount in cashflows:
    print(f"Payment Date: {date.date()}, Cash Flow: {amount} CAD")

# Plot the payments over time
plt.figure(figsize=(10, 6))

# Plotting the payments as bars
plt.bar(payment_dates, payment_amounts,color='blue', label='Coupon/Principal Payments',width = 50.0)

# Highlight the final payment (Principal + Coupon) in a different color
plt.bar(payment_dates[-1], payment_amounts[-1], color='red', label='Final Payment (Principal + Coupon)', width=50.0)

# Adding labels and title
plt.xlabel('Payment Date')
plt.ylabel('Cash Flow (CAD)')
plt.title('Bond Cash Flows Over Time')

# Format x-axis to show date properly
plt.xticks(rotation=45)
plt.tight_layout()

# Show legend
plt.legend()

# Show the plot
plt.show()

