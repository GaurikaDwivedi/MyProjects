from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from .models import IssuedBook
import logging

logger = logging.getLogger('celery')

@shared_task
def send_return_date_exceeded_emails():
    today = timezone.now().date()
    overdue_books = IssuedBook.objects.filter(return_date__lt=today)
    for issued_book in overdue_books:
        student = issued_book.student
        book = issued_book.book
        send_mail(
            'Book Return Reminder',
            f'Dear {student.name},\n\nThe return date for the book "{book.title}" has exceeded. Please return the book as soon as possible to avoid fines.\n\nThank you.',
            'library@example.com',
            [student.email],
            fail_silently=False,
        )
        logger.info(f'Email sent to {student.email} for overdue book {book.title}')

