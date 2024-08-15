import csv
from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist
from .models import User

@shared_task
def calculate_credit_score(aadhar_id):
    print("calculate_credit_score")
    
    try:
        user = User.objects.get(aadhar_id=aadhar_id)
        print("calculate_credit_score: USER", user)
    except ObjectDoesNotExist:
        print(f"User with aadhar_id {aadhar_id} does not exist.")
        return
    
    file_path = 'transactions_data.csv'
    print(f"Attempting to open file at: {file_path}")
    
    try:
        with open(file_path, 'r') as file:
            print("File opened successfully")
            reader = csv.DictReader(file)
            print("CSV DictReader initialized")
            total_balance = sum(
                int(row['Amount']) if row['Transaction_type'] == 'CREDIT' else -int(row['Amount'])
                for row in reader if row['AADHAR ID'] == aadhar_id
            )
            print("Total balance calculated:", total_balance)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return
    except Exception as e:
        print(f"An error occurred while processing the file: {e}")
        return
    
    if total_balance >= 1000000:
        credit_score = 900
    elif total_balance <= 100000:
        credit_score = 300
    else:
        credit_score = 300 + ((total_balance - 100000) // 15000) * 10
    
    print("calculate_credit_score: credit score", credit_score)
    
    user.credit_score = credit_score
    user.save()
    print("calculate_credit_score done")
