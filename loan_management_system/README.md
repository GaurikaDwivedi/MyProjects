# Loan Management System

This is a RESTful API for managing a loan system. It allows users to register, apply for loans, make payments, and retrieve loan statements.

## Features

- User Registration
- Loan Application
- EMI Calculation and Management
- Payment Processing
- Statement Retrieval

## API Endpoints

### Register User

#### Register a New User

- **URL**: `/register-user`
- **Method**: `POST`
- **Description**: Register new users.
- **Request Body**:
    ```json
    [
    {
        "name": "User 1",
        "email": "user1@example.com",
        "aadhar_id": "d425d4ba-82ba-4f05-974f-c28933f40bdf",
        "annual_income": 200000
    },
    {
        "name": "User 2",
        "email": "user2@example.com",
        "aadhar_id": "70ff859b-95b3-48b8-a162-2547987c6a88",
         "annual_income": 2000000
    }
    ...
    ]
    ```
- **Response**:
    ```json
    {
        "Created Users": [
            {
                "unique_user_id": "123456789012"
            }
        ],
        "Errors": []
    }
    ```

### Get All Users

#### Retrieve All Users

- **URL**: `/users`
- **Method**: `GET`
- **Description**: Get a list of all users.
- **Response**:
    ```json
    [
    {
        "id": "5f789552-4009-42b8-b24a-a05c8108d982",
        "aadhar_id": "d425d4ba-82ba-4f05-974f-c28933f40bdf",
        "name": "User 1",
        "email": "user1@example.com",
        "annual_income": "200000.00",
        "credit_score": 300
    },
    {
        "id": "03b0f04c-aa6b-4b55-8ef4-3500f3431c83",
        "aadhar_id": "70ff859b-95b3-48b8-a162-2547987c6a88",
        "name": "User 2",
        "email": "user2@example.com",
        "annual_income": "2000000.00",
        "credit_score": 400
    }
    ...
    ]
    ```

### Apply for a Loan

#### Apply for a Loan

- **URL**: `/apply_loan`
- **Method**: `POST`
- **Description**: Apply for a loan.
- **Request Body**:
    ```json
        {
        "aadhar_id": "6a6c86be-81d9-4bce-af3c-c32b8c6b5f34",
        "loan_type": "Home",
        "amount": 500000,
        "interest_rate": 8.5,
        "term_period": 36,
        "disbursement_date": "2024-08-15"
    }
    ```
- **Response**:
    ```json
    {
    "Loan_id": "96ed27e3-58c9-41e6-8867-9a42e99bd579",
    "Due_dates": [
        {
            "id": "b2a80827-6ee6-4f8c-bea0-21089d957e6c",
            "due_date": "2024-09-14",
            "principal_due": "11527.78",
            "interest_due": "3541.67",
            "amount_due": "15069.44",
            "status": "Unpaid",
            "loan": "96ed27e3-58c9-41e6-8867-9a42e99bd579"
        },
        {
            "id": "b8431117-f2c1-4d91-a2c0-fbc3681c3fd7",
            "due_date": "2024-10-14",
            "principal_due": "11609.43",
            "interest_due": "3460.01",
            "amount_due": "15069.44",
            "status": "Unpaid",
            "loan": "96ed27e3-58c9-41e6-8867-9a42e99bd579"
        }
        ....
    ]
    }
    ```

### Make Payment

#### Make a Payment

- **URL**: `/make_payment`
- **Method**: `POST`
- **Description**: Make a payment for an EMI.
- **Request Body**:
    ```json
    {
        "emi_id": "b2a80827-6ee6-4f8c-bea0-21089d957e6c",
        "amount": 15069.44,
        "payment_date": "2024-09-11"
    }
    ```
- **Response**:
    ```json
    {
        "Message": "Payment recorded"
    }
    ```

### Get Loan Statement

#### Retrieve Loan Statement

- **URL**: `/statement/<int:loan_id>`
- **Method**: `GET`
- **Description**: Get the statement of a loan, including past and upcoming emis.
- **Response**:
    ```json
    {
    "Loan Statement": [
        {
            "id": "b2a80827-6ee6-4f8c-bea0-21089d957e6c",
            "due_date": "2024-09-14",
            "principal_due": "11527.78",
            "interest_due": "3541.67",
            "amount_due": "15069.44",
            "status": "Paid",
            "loan": "96ed27e3-58c9-41e6-8867-9a42e99bd579"
        },
        {
            "id": "b8431117-f2c1-4d91-a2c0-fbc3681c3fd7",
            "due_date": "2024-10-14",
            "principal_due": "11609.43",
            "interest_due": "3460.01",
            "amount_due": "15069.44",
            "status": "Unpaid",
            "loan": "96ed27e3-58c9-41e6-8867-9a42e99bd579"
        }
        ...
        ]
        }
    ```

## Setup Instructions

1. **Clone the repository**:
    ```bash
    git clone <repository_url>
    ```

2. **Navigate to the project directory**:
    ```bash
    cd loan_management_system
    ```

3. **Apply migrations**:
    ```bash
    python manage.py migrate
    ```

4. **Run the development server**:
    ```bash
    python manage.py runserver
    ```
5. **Running Celery**:
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
        Open two terminal windows: In the first terminal, start the Celery worker:
        ```bash
        celery -A loan_management_system worker --loglevel=info
        ```
        In the second terminal, start Celery Beat (scheduler):
        ```bash
        celery -A loan_management_system beat --loglevel=info
        ```
6. **Access the API**:
    Visit `http://127.0.0.1:8000/` to access the API endpoints.
## Note

Running Celery along with the server is required because the credit score is calculated via Celery task.

## Testing

To test the API endpoints, you can use tools like Postman or curl. Ensure you include the required data for each endpoint.

---

This README provides a detailed overview of the API endpoints, including request methods, sample request bodies, and expected responses, along with setup instructions for running the project locally.
