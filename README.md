# Address Book API

This is a simple FastAPI application that provides an address book API. Users can create, read, update, and delete addresses, as well as retrieve addresses within a given distance from a specified location. The application includes user authentication and authorization using JSON Web Tokens (JWT).

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Setup

1. Clone the repository: `https://github.com/srb1998/address-book-api.git`
2. Navigate to the project directory: `cd address-book-api`
3. Install the required dependencies: `pip install -r requirements.txt`

## Running the Application

1. Start the FastAPI server: `uvicorn main:app --reload`
2. Access the Swagger documentation at `http://localhost:8000/docs`.

## API Endpoints

- `POST /signup/`: Create a new user account
- `POST /login/`: Obtain an access token by providing username and password
- `POST /addresses/`: Create a new address (requires authentication)
- `GET /addresses/`: Retrieve all addresses (requires authentication)
- `GET /addresses/{address_id}`: Retrieve a specific address by ID (requires authentication)
- `PUT /addresses/{address_id}`: Update an existing address (requires authentication)
- `DELETE /addresses/{address_id}`: Delete an address (requires authentication)
- `GET /addresses/nearby/`: Retrieve addresses within a given distance and location (requires authentication)

## Authentication

The application uses the OAuth2PasswordBearer scheme for authentication. To authorize requests in the Swagger UI, follow these steps:

1. Expand the "OAuth2PasswordBearer (OAuth2, password)" section.
2. Enter your username and password in the respective fields.
3. Click the "Authorize" button.

The Swagger UI will obtain an access token for you and use it to authenticate subsequent requests.

Note- Login endpoint can use used to get Access_token can be useful for other clients (e.g., mobile apps, third-party integrations) that need to obtain an access token by providing username and password. Use SECRET_KEY = 17d27b01e79d35c1bb2be25d4287881842515137f6237dddc6569c110b979615 on your .env