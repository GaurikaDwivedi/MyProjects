from django.db import models
from django.utils import timezone

class Book(models.Model):
    isbn = models.PositiveIntegerField()
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    publication_year = models.PositiveIntegerField()
    available_count = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.title

class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField()

    def __str__(self):
        return self.name

class IssuedBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    issue_date = models.DateField(default=timezone.now)
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.book.title} - {self.student.name}"
