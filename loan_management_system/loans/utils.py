from datetime import timedelta
from .models import EMI
from decimal import Decimal


def calculate_emis(loan):
    monthly_income = Decimal(loan.user.annual_income) / 12
    max_emi = Decimal(0.6) * monthly_income
    emi_amount = min(max_emi, loan.amount * (Decimal(1) + (loan.interest_rate / Decimal(100))) / loan.term_period)
    emis = []
    principal_remaining = loan.amount
    for month in range(1, loan.term_period + 1):
        interest_due = principal_remaining * (loan.interest_rate / Decimal(100)) / 12
        principal_due = emi_amount - interest_due
        emi_date = loan.disbursement_date + timedelta(days=30 * month)
        emis.append(EMI(
            loan=loan,
            due_date=emi_date,
            principal_due=principal_due,
            interest_due=interest_due,
            amount_due=emi_amount if month != loan.term_period else principal_remaining + interest_due,
            status='Unpaid'
        ))
        principal_remaining -= principal_due
    return emis
