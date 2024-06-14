from django.urls import path
from .views import BookListView,BookDetailView,StudentListView,IssueBookView,ReturnBookView,StudentDetailView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
# from rest_framework.authtoken.views import obtain_auth_token
urlpatterns = [
    path('books/', BookListView.as_view(), name='book_list'),
    path('book/<int:isbn>/', BookDetailView.as_view(), name='book-detail'),
    path('students/', StudentListView.as_view(), name='student_list'),
    path('students/<int:student_id>/', StudentDetailView.as_view(), name='student-detail-view'),
    path('issue_book/', IssueBookView.as_view(), name='issue_book'),
    path('issue_book/', IssueBookView.as_view(), name='issued_book_list'),
    path('issue_book/<int:isbn>/', IssueBookView.as_view(), name='issued_book_detail'),
    path('return_book/<int:isbn>/<int:student_id>/', ReturnBookView.as_view(), name='return_book'),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('auth/login/', obtain_auth_token, name='create_token'),

]