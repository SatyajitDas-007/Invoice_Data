# Django Rest Framework Invoice API

This is a Django Rest Framework project that provides APIs for managing invoices and their details.

## Requirements

- Python (3.6+)
- Django (3.0+)
- Django Rest Framework (3.12+)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/SatyajitDas-007/Invoice_Data.git
   ```

2. Navigate to the project directory:

   ```bash
   cd Invoice_Data
   ```

3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Apply database migrations:

   ```bash
   python manage.py migrate
   ```

5. Load initial data (optional):

   ```bash
   python manage.py loaddata db.json
   ```

6. Run the development server:

   ```bash
   python manage.py runserver
   ```

## Usage

- Access the API root at `http://localhost:8000/api/`
- Endpoints:
  - `http://localhost:8000/api/invoices/` (GET, POST)
  - `http://localhost:8000/api/invoices/{id}/` (GET, PUT, DELETE)

## API Documentation

- API documentation is automatically generated using Django Rest Framework's built-in tools.
- You can access the API documentation at `http://localhost:8000/swagger/` or `http://localhost:8000/redoc/`.

## Testing

To run tests, use the following command:

```bash
python manage.py test
```

## Contributing

Contributions are welcome! Feel free to open issues or pull requests.
