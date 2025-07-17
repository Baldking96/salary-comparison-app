import streamlit as st

def calculate_income_tax(monthly_salary):
    gross_annual_salary = monthly_salary * 12
    taxable_income = gross_annual_salary * 0.90

    tax = 0

    if taxable_income <= 600000:
        tax = 0
    elif taxable_income <= 1200000:
        tax = 0.01 * (taxable_income - 600000)
    elif taxable_income <= 2200000:
        tax = 6000 + 0.11 * (taxable_income - 1200000)
    elif taxable_income <= 3200000:
        tax = 116000 + 0.23 * (taxable_income - 2200000)
    elif taxable_income <= 4100000:
        tax = 346000 + 0.30 * (taxable_income - 3200000)
    else:
        tax = 616000 + 0.35 * (taxable_income - 4100000)

    if taxable_income > 10000000:
        tax += 0.09 * tax

    return gross_annual_salary, taxable_income, tax


def calculate_remittance_conversion_fixed(monthly_salary_pkr, dollar_rate):
    salary_usd = monthly_salary_pkr / dollar_rate

    # Fixed deductions
    to_payoneer = salary_usd * 0.99       # 1% fee
    to_ubl = to_payoneer * 0.985          # 1.5% fee on Payoneer amount

    pkr_equivalent = to_ubl * dollar_rate
    tax = pkr_equivalent * 0.0025         # 0.25%
    total_pkr_after_deduction = pkr_equivalent - tax

    return {
        "Salary in USD": salary_usd,
        "Transfer to Payoneer (1%)": to_payoneer,
        "Transfer to UBL (1.5%)": to_ubl,
        "PKR Equivalent": pkr_equivalent,
        "Tax (.25%)": tax,
        "Final PKR Received": total_pkr_after_deduction
    }


# Streamlit UI
st.title("🇵🇰 Salary Tax vs Remittance Comparison Tool")
st.write("Compare your local taxed salary vs remittance (Payoneer → UBL) to see which is better.")

# Inputs
monthly_salary = st.number_input("Enter your monthly gross salary (PKR)", min_value=0.0, value=350000.0)
dollar_rate = st.number_input("Enter the current dollar rate", min_value=100.0, value=285.0)

if st.button("Compare Now"):
    # Local tax calculation
    annual, taxable, tax = calculate_income_tax(monthly_salary)
    monthly_tax = tax / 12
    monthly_after_tax = monthly_salary - monthly_tax

    st.subheader("📊 Local Salary (Taxed)")
    st.write(f"**Annual Salary:** Rs. {annual:,.2f}")
    st.write(f"**Taxable Income (after 10% medical exemption):** Rs. {taxable:,.2f}")
    st.write(f"**Total Annual Tax:** Rs. {tax:,.2f}")
    st.write(f"**Monthly Tax Deduction:** Rs. {monthly_tax:,.2f}")
    st.write(f"**Monthly Salary After Tax:** Rs. {monthly_after_tax:,.2f}")

    # Remittance calculation
    remittance = calculate_remittance_conversion_fixed(monthly_salary, dollar_rate)
    final_remit_pkr = remittance["Final PKR Received"]

    st.subheader("🌍 Remittance (Payoneer → UBL)")
    for label, value in remittance.items():
        if "PKR" in label or "Tax" in label:
            st.write(f"**{label}:** Rs. {value:,.2f}")
        else:
            st.write(f"**{label}:** {value:,.2f} USD")

    # Comparison
    st.subheader("⚖️ Final Comparison")
    difference = final_remit_pkr - monthly_after_tax
    st.write(f"**Difference (Remittance - Local):** Rs. {difference:,.2f}")
    if difference > 0:
        st.success("✅ Remittance is more beneficial.")
    elif difference < 0:
        st.error("❌ Local taxed salary is more beneficial.")
    else:
        st.info("⚖️ Both methods result in the same amount.")
