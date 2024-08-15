from django.urls import path
from .views import RegisterUserView, ApplyLoanView, MakePaymentView, GetStatementView, GetAllUsersView

urlpatterns = [
    path('register-user/', RegisterUserView.as_view(), name='register-user'),
    path('users/', GetAllUsersView.as_view(), name='get-all-users'),
    path('apply-loan/', ApplyLoanView.as_view(), name='apply-loan'),
    path('make-payment/', MakePaymentView.as_view(), name='make-payment'),
    path('get-statement/<uuid:loan_id>/', GetStatementView.as_view(), name='get-statement'),
]
