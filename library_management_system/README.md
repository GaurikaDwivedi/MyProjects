# Library Management System

This is a RESTful API for managing a library system. It allows users to perform CRUD operations on books and students, issue books to students, and return books and user authentication. The system includes a feature to remind students to return overdue books via email.

## Features

- User Registration & authentication.
- Book management: Add, update, delete, and list books.
- Student management: Add, update, delete, and list students.
- Book issuance: Issue books to students.
- Return management: Manage the return of issued books.
- Overdue notification: Send email reminders for overdue books.
  
## API Endpoints
### User Authentication

#### Register a New User

- **URL**: `/register`
- **Method**: `POST`
- **Description**: Register a new user.
- **Request Body**:
    ```json
    {
        "email": "user@example.com",
        "password": "password123",
        "name": "John",
    }
    ```

#### User Login

- **URL**: `/login`
- **Method**: `POST`
- **Description**: Authenticate user credentials and retrieve access tokens.
- **Request Body**:
    ```json
    {
        "email": "user@example.com",
        "password": "password123"
    }
    ```
- **Response**:
    ```json
    {
        "refresh": "refresh_token_string",
        "access": "access_token_string"
    }
    ```

#### Retrieve User Details

- **URL**: `/user`
- **Method**: `GET`
- **Description**: Retrieve details of the authenticated user using the access token.
- **Headers**: `Authorization: Bearer <access_token_string>`
- **Response**:
    ```json
    {
        "user_id": 1,
        "exp": 1623733629
        // Additional user details as needed
    }
    ```
### Book Endpoints

#### List All Books

- **URL**: `/books/`
- **Method**: `GET`
- **Description**: Retrieve a list of all books.
- **Response**:
    ```json
    [
        {
            "id": 1,
            "isbn": "100001",
            "title": "Book Title",
            "author": "Author Name",
            "publication_year": 2022,
            "available_count": 5
        },
        ...
    ]
    ```

#### Create Books in Bulk

- **URL**: `/books/`
- **Method**: `POST`
- **Description**: Create multiple new books.
- **Request Body**:
    ```json
    [
        {
            "isbn": "100001",
            "title": "New Book Title",
            "author": "Author Name",
            "publication_year": 2022,
            "available_count": 5
        },
        ...
    ]
    ```

#### Update Books in Bulk

- **URL**: `/books/`
- **Method**: `PUT`
- **Description**: Update multiple books by ISBN.
- **Request Body**:
    ```json
    [
        {
            "isbn": "100001",
            "title": "Updated Book Title",
            "author": "Updated Author",
            "publication_year": 2023,
            "available_count": 4
        },
        ...
    ]
    ```

#### Delete Books in Bulk

- **URL**: `/books/`
- **Method**: `DELETE`
- **Description**: Delete multiple books by ISBN.
- **Request Body**:
    ```json
    {
        "isbn_nos": ["100001", "100002"]
    }
    ```

#### Get Book Details

- **URL**: `/book/<int:isbn>/`
- **Method**: `GET`
- **Description**: Retrieve details of a specific book by ISBN.
- **Response**:
    ```json
    {
        "id": 1,
        "isbn": "100001",
        "title": "Book Title",
        "author": "Author Name",
        "publication_year": 2022,
        "available_count": 5
    }
    ```

#### Update Book Details

- **URL**: `/book/<int:isbn>/`
- **Method**: `PUT`
- **Description**: Update details of a specific book by ISBN.
- **Request Body**:
    ```json
    {
        "isbn": "100001",
        "title": "Updated Book Title",
        "author": "Updated Author",
        "publication_year": 2023,
        "available_count": 4
    }
    ```

#### Delete Book

- **URL**: `/book/<int:isbn>/`
- **Method**: `DELETE`
- **Description**: Delete a specific book by ISBN.
- **Response**:
    ```json
    {
        "message": "Book deleted successfully"
    }
    ```

### Student Endpoints

#### List All Students

- **URL**: `/students/`
- **Method**: `GET`
- **Description**: Retrieve a list of all students.
- **Response**:
    ```json
    [
        {
            "id": 1,
            "name": "John Doe",
            "roll_number": "101",
            "email": "abc@gmail.com"
        },
        ...
    ]
    ```

#### Create Students in Bulk

- **URL**: `/students/`
- **Method**: `POST`
- **Description**: Create multiple new students.
- **Request Body**:
    ```json
    [
        {
            "name": "John Doe",
            "roll_number": "101",
            "email": "john@example.com"
        },
        ...
    ]
    ```

#### Update Students in Bulk

- **URL**: `/students/`
- **Method**: `PUT`
- **Description**: Update multiple students by roll number.
- **Request Body**:
    ```json
    [
        {
            "roll_number": "101",
            "name": "John Doe Updated",
            "email": "john_updated@example.com"
        },
        ...
    ]
    ```

#### Delete Students in Bulk

- **URL**: `/students/`
- **Method**: `DELETE`
- **Description**: Delete multiple students by roll number.
- **Request Body**:
    ```json
    {
        "roll_numbers": ["101", "102"]
    }
    ```

#### Get Student Details

- **URL**: `/students/<int:student_roll_number>/`
- **Method**: `GET`
- **Description**: Retrieve details of a specific student by roll_number, including issued book information.
- **Response**:
    ```json
    {
        "student_info": {
            "id": 1,
            "name": "John Doe",
            "roll_number": "101",
            "email": "john@example.com"
        },
        "issued_books": [
            {
                "book_title": "Book Title",
                "student_name": "John Doe",
                "issue_date": "2024-04-09",
                "return_date": "2024-04-14"
            }
        ]
    }
    ```

#### Update Student Details

- **URL**: `/students/<int:roll_number>/`
- **Method**: `PUT`
- **Description**: Update details of a specific student by roll_number.
- **Request Body**:
    ```json
    {
        "name": "John Doe Updated",
        "roll_number": "101",
        "email": "john_updated@example.com"
    }
    ```

#### Delete Student

- **URL**: `/students/<int:student_roll_number>/`
- **Method**: `DELETE`
- **Description**: Delete a specific student by roll_number.
- **Response**:
    ```json
    {
        "message": "Student deleted successfully"
    }
    ```

### Book Issuing and Returning Endpoints

#### Issue a Book

- **URL**: `/issue_book/`
- **Method**: `POST`
- **Description**: Issue a book to a student.
- **Request Body**:
    ```json
    {
        "isbn": "100001",
        "roll_number": 101
    }
    ```
- **Response**:
    ```json
    {
        "message": "Book issued successfully!"
    }
    ```

#### List All Issued Books

- **URL**: `/issue_book_list/`
- **Method**: `GET`
- **Description**: Retrieve a list of all issued books.
- **Response**:
    ```json
    [
        {
            "book_title": "Book Title",
            "student_name": "John Doe",
            "issue_date": "2024-04-09",
            "return_date": "2024-04-14"
        },
        ...
    ]
    ```
#### Get Issued Books by ISBN

- **URL**: `/issue_book_detail/<int:isbn>/<int:roll_number>/`
- **Method**: `GET`
- **Description**: Retrieve a list of issued books by ISBN.
- **Response**:
    ```json
    {
    "id": 4,
    "book": {
        "id": 4,
        "isbn": 100001,
        "title": "Updated Book Title",
        "author": "Updated Author",
        "publication_year": 2022,
        "available_count": 6
    },
    "student": {
        "id": 1,
        "name": "John Doe",
        "roll_number": "101",
        "email": "johnd@gmail.com"
    },
    "issue_date": "2024-04-09",
    "return_date": "2024-04-14"
    }
    ```
#### Return a Book

- **URL**: `/return_book/<int:isbn>/<int:roll_number>/`
- **Method**: `POST`
- **Description**: Return a book by ISBN and student roll_number.
- **Response**:
    ```json
    {
        "message": "Book returned successfully without any fine."
    }
    ```
## Running Celery
### Steps
1. **Install Celery & Redis**:
   ```bash
     pip install celery
    ```
    MacOS (using Homebrew):
   ```bash
     brew install redis
    ```
3. **Start the Redis Server**:
     MacOS:
    ```bash
     redis-server
    ```
4. **Celery Configuration**: Already present in celery.py file
5. **Running Celery Worker and Beat**:
     Open two terminal windows:
   In the first terminal, start the Celery worker:
    ```bash
     celery -A library_management_system worker --loglevel=info
    ```
   In the second terminal, start Celery Beat (scheduler):
   ```bash
     celery -A library_management_system beat --loglevel=info
    ```
6. **Check Celery Worker Logs**:
   When you run your Celery worker, you can observe the logs to see the execution of tasks.You should see log entries indicating when a task starts and completes.
   For example:
       [2024-06-15 07:19:05,047: INFO/ForkPoolWorker-8] Email sent to john@gmail.com for overdue book Updated Book Title
       [2024-06-15 07:19:05,054: INFO/ForkPoolWorker-8] Task library.tasks.send_return_date_exceeded_emails[3eff238b-b306-4fd7-8e74-1dbcf604b982] succeeded in 5.031857666792348s: None
7. **Testing Celery Tasks Locally**:
   To run the Celery task manually for testing, you can use the Django shell: 
    ```bash
    python manage.py shell
    ```
   Then, import and run your task:
   ```bash
    from your_project_name.tasks import send_return_date_exceeded_emails
    send_return_date_exceeded_emails()
    ```

## Setup Instructions

1. **Clone the repository**:
    ```bash
    git clone <repository_url>
    ```
2. **Navigate to the project directory**:
    ```bash
    cd library_management_system
    ```
3. **Apply migrations**:
    ```bash
    python manage.py migrate
    ```
4. **Run the development server**:
    ```bash
    python manage.py runserver
    ```

5. **Access the API**:
    Visit `http://127.0.0.1:8000/` to access the API endpoints.
   
6. **Run celery**:

## Testing

To test the API endpoints, you can use tools like Postman or curl. Ensure you include the required authentication headers for the protected endpoints.

---

This README provides a detailed overview of the API endpoints, including request methods, sample request bodies, and expected responses, along with setup instructions for running the project locally.
