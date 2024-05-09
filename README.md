# Vendor Management System With Performance Metrics

This document provides detailed instructions on how to set up, configure, and run this project. Follow these steps to ensure your development environment is properly configured. All API endpoints require token-based authentication, ensuring that only authorized users can access the API. This document also provides detailed instructions on how to interact with the API endpoints in the Django project.

## Prerequisites

Before you begin, make sure you have Python installed on your system. This project requires Python 3.8 or higher. You can download Python from [python.org](https://www.python.org/downloads/).

## Setup Instructions

### 1. Clone the Repository

Clone this repository to your local machine using git:

```bash
git clone https://github.com/yourusername/yourprojectname.git
cd yourprojectname
```

### 2. Virtual Environment Setup

It's recommended to use a virtual environment to manage the dependencies separately from other Python projects. Create and activate a virtual environment by running:

#### For macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### For Windows:

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

### 3. Install Dependencies

With the virtual environment activated, install the project dependencies using:

```bash
pip install -r requirements.txt
```

### 4. Database

This project uses SQLite by default, so no initial setup is required for a development environment.

### 5. Running Migrations

To set up your database tables according to the models defined in the project, run the following command:

```bash
python manage.py migrate
```

### Creating a Superuser Account

Before accessing the API, you must create a superuser account. This account will also be used to generate an authentication token.

```bash
python manage.py createsuperuser
```

Follow the prompts to set the username, email, and password.

### 7. Running the Development Server

Start the development server to see if the application is running correctly:

```bash
python manage.py runserver
```

This will start the server on http://127.0.0.1:8000/ by default.

### Obtaining an Authentication Token

1. **Generate a Token**: After creating your superuser account, use the following endpoint to obtain your authentication token:

   ```
   POST /api/token-auth/
   ```

   Send a POST request with your username and password:

   ```bash
   curl -X POST -d "username=<your_username>&password=<your_password>" http://localhost:8000/api/token-auth/
   ```

   The response will include a token, which you will use in subsequent requests to the API.

2. **Using the Token**: For all API requests, include the token in the header:

   ```
   Authorization: Token <your_token_here>
   ```

## API Endpoints

Here are the available API endpoints and how to interact with them using `curl`. Replace `<your_token_here>` with the token you obtained from the token authentication endpoint.

### Vendor Endpoints

- **List All Vendors**:

  ```
  GET /api/vendors/
  ```

  ```bash
  curl -H "Authorization: Token <your_token_here>" http://localhost:8000/api/vendors/
  ```

- **Create a New Vendor**:

  ```
  PUT /api/vendors/
  ```

  ```bash
  curl -X PUT -H "Authorization: Token <your_token_here>" -d @vendor_data.json http://localhost:8000/api/vendors/
  ```

  Replace `vendor_data.json` with your JSON file containing vendor details.

- **Retrieve Specific Vendor Details**:

  ```
  GET /api/vendors/{vendor_id}/
  ```

  ```bash
  curl -H "Authorization: Token <your_token_here>" http://localhost:8000/api/vendors/{vendor_id}/
  ```

- **Update Vendor Details**:

  ```
  PUT /api/vendors/{vendor_id}/
  ```

  ```bash
  curl -X PUT -H "Authorization: Token <your_token_here>" -d @update_data.json http://localhost:8000/api/vendors/{vendor_id}/
  ```

- **Delete a Vendor**:
  ```
  DELETE /api/vendors/{vendor_id}/
  ```
  ```bash
  curl -X DELETE -H "Authorization: Token <your_token_here}" http://localhost:8000/api/vendors/{vendor_id}/
  ```

### Purchase Order Endpoints

- **Create a Purchase Order**:

  ```
  POST /api/purchase_orders/
  ```

  ```bash
  curl -X POST -H "Authorization: Token <your_token_here>" -d @po_data.json http://localhost:8000/api/purchase_orders/
  ```

- **List All Purchase Orders**:

  ```
  GET /api/purchase_orders/
  ```

  the endpoint is avalible with query parameters for optional filtering by vendor id add `?filter_by_vendor_id=<vendor_id>` for optional filter functionality

  ```bash
  curl -H "Authorization: Token <your_token_here>" http://localhost:8000/api/purchase_orders/?filter_by_vendor_id=<vendor_id>
  ```

- **Retrieve Specific Purchase Order Details**:

  ```
  GET /api/purchase_orders/{po_id}/
  ```

  ```bash
  curl -H "Authorization: Token <your_token_here>" http://localhost:8000/api/purchase_orders/{po_id}/
  ```

- **Update a Purchase Order**:

  ```
  PUT /api/purchase_orders/{po_id}/
  ```

  ```bash
  curl -X PUT -H "Authorization: Token <your_token_here>" -d @update_po_data.json http://localhost:8000/api/purchase_orders/{po_id}/
  ```

- **Delete a Purchase Order**:
  ```
  DELETE /api/purchase_orders/{po_id}/
  ```
  ```bash
  curl -X DELETE -H "Authorization: Token <your_token_here>" http://localhost:8000/api/purchase_orders/{po_id}/
  ```

### Vendor Performance Metrics

- **Retrieve a Vendor's Performance Metrics**:
  ```
  GET /api/vendors/{vendor_id}/performance
  ```
  ```bash
  curl -H "Authorization: Token <your_token_here>" http://localhost:8000/api/vendors/{vendor_id}/performance
  ```

### 8. Running Tests

Ensure that the application works as expected by running the automated tests. Execute:

```bash
python manage.py test
```

## Conclusion

By following these setup instructions, you should have a functional Django development environment. This setup will allow you to develop and test your Django application in isolation, ensuring that your deployments are as smooth and error-free as possible.
