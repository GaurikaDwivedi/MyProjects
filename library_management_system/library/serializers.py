from rest_framework import serializers
from .models import Book, Student, IssuedBook

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id','isbn', 'title', 'author', 'publication_year', 'available_count']

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'roll_number', 'email']

class IssuedBookSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    student_name = serializers.CharField(source='student.name', read_only=True)

    class Meta:
        model = IssuedBook
        fields = ['book_title', 'student_name', 'issue_date', 'return_date']

class IssuedBookDetailSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    book = BookSerializer(read_only=True)

    class Meta:
        model = IssuedBook
        fields = ['id', 'book', 'student', 'issue_date', 'return_date']