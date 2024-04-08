# Address Book API

This is a simple FastAPI application that provides an address book API. Users can create, read, update, and delete addresses, as well as retrieve addresses within a given distance from a specified location.

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Setup

1. Clone the repository:
https://github.com/srb1998/address-book-api.git

2. Navigate to the project directory:
cd address

3. Install the required dependencies:
pip install -r requirements.txt

## Running the Application

1. Start the FastAPI server:
uvicorn app.main:app --reload

2. Access the Swagger documentation at `http://localhost:8000/docs`.

## API Endpoints

- `POST /addresses/`: Create a new address
- `GET /addresses/`: Retrieve all addresses
- `GET /addresses/{address_id}`: Retrieve a specific address by ID
- `PUT /addresses/{address_id}`: Update an existing address
- `DELETE /addresses/{address_id}`: Delete an address
- `GET /addresses/nearby/`: Retrieve addresses within a given distance and location



