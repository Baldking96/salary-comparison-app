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


if __name__ == "__main__":
    # Inputs
    monthly_salary = float(input("Enter your monthly gross salary (PKR): "))
    dollar_rate = float(input("Enter the current dollar rate (e.g. 284.8): "))

    # Local Tax Calculation
    annual, taxable, tax = calculate_income_tax(monthly_salary)
    monthly_tax = tax / 12
    monthly_salary_after_tax = monthly_salary - monthly_tax

    print("\n--- Income Tax Calculation (Local) ---")
    print(f"Annual Salary: Rs. {annual:,.2f}")
    print(f"Taxable income (after 10% medical exemption): Rs. {taxable:,.2f}")
    print(f"Total Annual Income Tax: Rs. {tax:,.2f}")
    print(f"Monthly Tax Deduction: Rs. {monthly_tax:,.2f}")
    print(f"Monthly Salary After Tax: Rs. {monthly_salary_after_tax:,.2f}")

    # Remittance Comparison
    remittance = calculate_remittance_conversion_fixed(monthly_salary, dollar_rate)
    remittance_salary = remittance["Final PKR Received"]

    print("\n--- Remittance Comparison ---")
    for key, value in remittance.items():
        if "PKR" in key or "Tax" in key:
            print(f"{key}: Rs. {value:,.2f}")
        else:
            print(f"{key}: {value:,.2f}")

    # Comparison
    difference = remittance_salary - monthly_salary_after_tax
    print("\n--- Comparison ---")
    print(f"Difference (Remittance - Local): Rs. {difference:,.2f}")

    if difference > 0:
        print("✅ Remittance is more beneficial.")
    elif difference < 0:
        print("❌ Local taxed salary is more beneficial.")
    else:
        print("⚖️ Both methods result in the same amount.")
