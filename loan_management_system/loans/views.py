from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from .models import User, Loan, EMI, Payment
from .serializers import UserSerializer, LoanSerializer, PaymentSerializer, EMISerializer
from .tasks import calculate_credit_score
from .utils import calculate_emis
from rest_framework.views import APIView
from django.db import transaction
from decimal import Decimal

class RegisterUserView(APIView):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        users_data = request.data
        if not users_data:
            return Response({'Error': 'No user data provided.'}, status=status.HTTP_400_BAD_REQUEST)
        
        created_users = []
        errors = []
        
        for user_data in users_data:
            aadhar_id = user_data.get('aadhar_id')
            if User.objects.filter(aadhar_id=aadhar_id).exists():
                errors.append({'aadhar_id': aadhar_id, 'Error': 'User with this Aadhar ID already exists.'})
                continue
            
            serializer = UserSerializer(data=user_data)
            if serializer.is_valid():
                try:
                    user = serializer.save()
                    calculate_credit_score.delay(user.aadhar_id)
                    created_users.append({'unique_user_id': user.aadhar_id})
                except Exception as e:
                    transaction.set_rollback(True)
                    errors.append({'aadhar_id': aadhar_id, 'Error': str(e)})
            else:
                errors.append({'aadhar_id': aadhar_id, 'Error': serializer.errors})
        
        if errors:
            return Response({'Created Users': created_users, 'Errors': errors}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'Created Users': created_users}, status=status.HTTP_201_CREATED)
  
class GetAllUsersView(APIView):
    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ApplyLoanView(APIView):
    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, aadhar_id=request.data.get('aadhar_id'))
        if user.credit_score < 450:
            return Response({'Error': 'Credit score too low'}, status=status.HTTP_400_BAD_REQUEST)
        if user.annual_income < 150000:
            return Response({'Error': 'Income too low'}, status=status.HTTP_400_BAD_REQUEST)

        loan_serializer = LoanSerializer(data=request.data)
        if loan_serializer.is_valid():
            loan = loan_serializer.save(user=user, status='Active')
            emis = calculate_emis(loan)
            for emi in emis:
                emi.save()
            emi_data = EMISerializer(emis, many=True).data
            return Response({'Loan_id': loan.id, 'Due_dates': emi_data}, status=status.HTTP_201_CREATED)
        return Response({'Error': loan_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class MakePaymentView(APIView):
    def post(self, request, *args, **kwargs):
        emi = get_object_or_404(EMI, id=request.data.get('emi_id'))
        if emi.status == 'Paid':
            return Response({'Error': 'EMI already paid'}, status=status.HTTP_400_BAD_REQUEST)
        if emi.loan.status == 'Closed':
            return Response({'Error': 'Loan is closed'}, status=status.HTTP_400_BAD_REQUEST)
        
        payment_amount = Decimal(request.data.get('amount', 0))
        payment_amount = round(payment_amount, 2)
        if payment_amount != emi.amount_due:
            return Response({'Error': f'The payment amount of {payment_amount} does not match the required EMI amount of {emi.amount_due}. Please ensure the full amount is paid.'}, status=status.HTTP_400_BAD_REQUEST)

        payment_data = request.data.copy()
        payment_data['emi'] = emi.id 
        payment_serializer = PaymentSerializer(data=payment_data)
        if payment_serializer.is_valid():
            payment = payment_serializer.save()
            emi.status = 'Paid'
            emi.save()
            return Response({'Message': 'Payment recorded'}, status=status.HTTP_201_CREATED)
        return Response({'Error': payment_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class GetStatementView(APIView):
    def get(self, request, loan_id, *args, **kwargs):
        loan = get_object_or_404(Loan, id=loan_id)

        # Fetch all EMIs for the loan
        all_emis = EMI.objects.filter(loan=loan)
        
        # Separate paid and unpaid EMIs
        past_transactions = all_emis.filter(status='Paid')
        upcoming_transactions = all_emis.filter(status='Unpaid')

        # Serialize the data
        # past_data = EMISerializer(past_transactions, many=True).data
        # upcoming_data = EMISerializer(upcoming_transactions, many=True).data
        all_emis_data = EMISerializer(all_emis, many=True).data

        return Response({
            'Loan Statement': all_emis_data
        }, status=status.HTTP_200_OK)
