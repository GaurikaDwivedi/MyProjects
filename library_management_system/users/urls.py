from django.urls import path
from .views import Register, LoginView, UserView

urlpatterns = [
    path('register', Register.as_view()),
    path('login', LoginView.as_view()),
    path('user', UserView.as_view())
]