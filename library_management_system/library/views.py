from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Book, Student, IssuedBook
from .serializers import BookSerializer, StudentSerializer, IssuedBookSerializer, IssuedBookDetailSerializer
from datetime import timedelta

class BookListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = BookSerializer(data=request.data, many=True)
        if serializer.is_valid():
            books = [Book(**book_data) for book_data in serializer.validated_data]
            Book.objects.bulk_create(books)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        books_data = request.data
        isbn_list = [book_data['isbn'] for book_data in books_data if 'isbn' in book_data]
        books = Book.objects.filter(isbn__in=isbn_list)
        books_dict = {book.isbn: book for book in books}

        updated_books = []

        for book_data in books_data:
            isbn = book_data.get('isbn')
            if not isbn or isbn not in books_dict:
                continue
            book = books_dict[isbn]
            for key, value in book_data.items():
                setattr(book, key, value)
            updated_books.append(book)

        if updated_books:
            Book.objects.bulk_update(updated_books, fields=['isbn', 'title', 'author', 'publication_year', 'available_count'])
            updated_serializer = BookSerializer(updated_books, many=True)
            return Response(updated_serializer.data, status=status.HTTP_200_OK)
        return Response({'message': 'No valid books found to update'}, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request):
        isbn_nos = request.data.get('isbn_nos', [])
        books = Book.objects.filter(isbn__in=isbn_nos)
        if books.exists():
            books.delete()
            return Response({'message': 'Books deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'message': 'No books found with the provided ISBN numbers'}, status=status.HTTP_404_NOT_FOUND)

class BookDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, isbn):
        book = get_object_or_404(Book, isbn=isbn)
        serializer = BookSerializer(book)
        return Response(serializer.data)
    
    def put(self, request, isbn):
        book = get_object_or_404(Book, isbn=isbn)
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, isbn):
        book = get_object_or_404(Book, isbn=isbn)
        book.delete()
        return Response({'message': 'Book deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
class StudentListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = StudentSerializer(data=request.data, many=True)
        if serializer.is_valid():
            students = [Student(**student_data) for student_data in serializer.validated_data]
            Student.objects.bulk_create(students)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        students_data = request.data
        roll_numbers = [student_data['roll_number'] for student_data in students_data if 'roll_number' in student_data]
        students = Student.objects.filter(roll_number__in=roll_numbers)
        students_dict = {student.roll_number: student for student in students}

        updated_students = []

        for student_data in students_data:
            roll_number = student_data.get('roll_number')
            if not roll_number or roll_number not in students_dict:
                continue
            student = students_dict[roll_number]
            for key, value in student_data.items():
                setattr(student, key, value)
            updated_students.append(student)

        if updated_students:
            Student.objects.bulk_update(updated_students, fields=['name', 'email'])
            updated_serializer = StudentSerializer(updated_students, many=True)
            return Response(updated_serializer.data, status=status.HTTP_200_OK)
        return Response({'message': 'No valid students found to update'}, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request):
        roll_numbers = request.data.get('roll_numbers', [])
        students = Student.objects.filter(roll_number__in=roll_numbers)
        if students.exists():
            students.delete()
            return Response({'message': 'Students deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'message': 'No students found with the provided roll numbers'}, status=status.HTTP_404_NOT_FOUND)
    
class StudentDetailView(APIView):
    def get(self, request, roll_number):
        student = get_object_or_404(Student, roll_number=roll_number)
        issued_books = IssuedBook.objects.filter(student=student)
        student_serializer = StudentSerializer(student)
        issued_books_serializer = IssuedBookSerializer(issued_books, many=True)
        response_data = {
            'student_info': student_serializer.data,
            'issued_books': issued_books_serializer.data
        }
        return Response(response_data)
    
    def put(self, request, roll_number):
        student = get_object_or_404(Student, roll_number=roll_number)
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
    
    def delete(self, request, roll_number):
        student = get_object_or_404(Student, roll_number=roll_number)
        student.delete()
        return Response({'message': 'Student deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

class IssueBookView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        isbn = data.get('isbn')
        student_roll_number = data.get('roll_number')

        # Check if the book is available
        book = get_object_or_404(Book, isbn=isbn)
        if book.available_count <= 0:
            return Response({'message': 'The requested book is not available.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the student already holds the book
        existing_issued_book = IssuedBook.objects.filter(book=book, student__roll_number=student_roll_number).exists()
        if existing_issued_book:
            return Response({'message': 'You have already issued this book.'}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the student
        student = get_object_or_404(Student, roll_number=student_roll_number)

        # Issue the book
        book.available_count -= 1
        book.save()
        issue_date = timezone.now().date()
        return_date = issue_date + timedelta(days=5)
        IssuedBook.objects.create(book=book, student=student, issue_date=issue_date, return_date=return_date)
        return Response({'message': 'Book issued successfully!'}, status=status.HTTP_201_CREATED)

    # List of all issued books
    def get(self, request):
        issuedBooks = IssuedBook.objects.all()
        serializer = IssuedBookSerializer(issuedBooks, many=True)
        return Response(serializer.data)

class IssuedBookDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, isbn, roll_number):
        issued_book = get_object_or_404(IssuedBook, book__isbn=isbn, student__roll_number=roll_number)
        serializer = IssuedBookDetailSerializer(issued_book)
        return Response(serializer.data)
    
class ReturnBookView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, isbn, roll_number):
        issued_book = get_object_or_404(IssuedBook, book__isbn=isbn, student__roll_number=roll_number)
        book = issued_book.book
        book.available_count += 1
        book.save()
        days_overdue = (timezone.now().date() - issued_book.issue_date).days
        if days_overdue > 5:
            fine = days_overdue - 5  # Calculate the fine (assuming $1 per day)
            issued_book.delete()
            return Response({'message': f'Book returned successfully with a fine of ${fine}.'})
        else:
            issued_book.delete()
            return Response({'message': 'Book returned successfully without any fine.'})
