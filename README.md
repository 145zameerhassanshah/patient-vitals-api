# Patient Vitals API

A REST API built with FastAPI for receiving, validating, storing, retrieving, and summarizing patient health metrics.

The project demonstrates REST API development, structured request validation, SQLite persistence, API documentation, aggregation, and automated testing.

> **Educational Use:** This project uses synthetic or de-identified example data and is not intended for clinical diagnosis, treatment, or production healthcare use.

## Features

- FastAPI REST service
- SQLite persistent data storage
- Pydantic request validation
- Nested blood-pressure data model
- Custom `400 Bad Request` responses
- UTC timestamps
- Patient vitals history
- Optional result limiting
- Patient-level summary statistics
- Swagger/OpenAPI documentation
- Automated Pytest integration tests

## Project Structure

```text
patient-vitals-api/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── schemas.py
│   ├── database.py
│   └── services.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_api.py
│
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
```

## Technology Stack

- Python
- FastAPI
- Uvicorn
- Pydantic
- SQLite
- Pytest
- HTTPX / FastAPI TestClient

## API Endpoints

### 1. Health Check

```http
GET /health
```

Returns the API status and current UTC timestamp.

Example:

```json
{
  "status": "ok",
  "timestamp": "2026-10-22T10:30:00+00:00"
}
```

### 2. Submit Patient Vitals

```http
POST /vitals
```

Required JSON payload:

```json
{
  "patient_id": "P001",
  "age": 45,
  "blood_pressure": {
    "systolic": 120,
    "diastolic": 80
  },
  "glucose_level": 105.5
}
```

A successful request returns:

```text
201 Created
```

The record is stored in SQLite together with a UTC timestamp.

### 3. Retrieve Patient Vitals History

```http
GET /patients/{patient_id}/vitals
```

Example:

```http
GET /patients/P001/vitals
```

Returns all stored vitals records for the specified patient.

An optional `limit` query parameter can restrict the number of returned records:

```http
GET /patients/P001/vitals?limit=2
```

### 4. Retrieve Patient Summary

```http
GET /patients/{patient_id}/summary
```

Example:

```http
GET /patients/P001/summary
```

Example response:

```json
{
  "patient_id": "P001",
  "average_systolic": 125.0,
  "average_diastolic": 82.0,
  "average_glucose": 110.0,
  "total_records": 2
}
```

The summary is calculated from all records associated with the specified patient.

## Validation Rules

Invalid requests return:

```text
400 Bad Request
```

The API validates the following requirements:

- `patient_id` must be present and must not be empty.
- `age` must be an integer between `0` and `120`.
- `blood_pressure.systolic` must be between `50` and `300`.
- `blood_pressure.diastolic` must be between `30` and `200`.
- `glucose_level` must be greater than `0`.

Example invalid request:

```json
{
  "patient_id": "",
  "age": 150,
  "blood_pressure": {
    "systolic": 350,
    "diastolic": 20
  },
  "glucose_level": 0
}
```

The application defines a custom FastAPI validation exception handler because FastAPI normally returns `422 Unprocessable Entity` for request validation errors, while this project's requirements specify `400 Bad Request`.

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/patient-vitals-api.git
cd patient-vitals-api
```

Create a Python virtual environment:

```powershell
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

## Run the API

Start the FastAPI development server:

```powershell
python -m uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

## Swagger Documentation

Open:

```text
http://127.0.0.1:8000/docs
```

Swagger UI allows all API endpoints to be tested interactively.

OpenAPI documentation can also be accessed through:

```text
http://127.0.0.1:8000/openapi.json
```

## Manual Testing with curl

### Health Check

```bash
curl http://127.0.0.1:8000/health
```

### Submit Vitals

```bash
curl -X POST http://127.0.0.1:8000/vitals \
-H "Content-Type: application/json" \
-d "{\"patient_id\":\"P001\",\"age\":45,\"blood_pressure\":{\"systolic\":120,\"diastolic\":80},\"glucose_level\":105.5}"
```

### Retrieve Patient History

```bash
curl http://127.0.0.1:8000/patients/P001/vitals
```

### Retrieve Limited History

```bash
curl "http://127.0.0.1:8000/patients/P001/vitals?limit=1"
```

### Retrieve Patient Summary

```bash
curl http://127.0.0.1:8000/patients/P001/summary
```

## Automated Testing

The project includes automated API tests using Pytest and FastAPI TestClient.

Run:

```powershell
pytest
```

The tests cover:

- API health status
- valid vitals submissions
- SQLite persistence
- patient history retrieval
- `limit` query parameter
- summary calculations
- empty patient IDs
- missing patient IDs
- age outside the allowed range
- invalid systolic values
- invalid diastolic values
- non-positive glucose values
- invalid data types
- unknown patient summary requests

Tests use an isolated temporary SQLite database to avoid modifying development data.

## Example Summary Calculation

Consider two records for `P001`.

Record 1:

```text
Systolic: 120
Diastolic: 80
Glucose: 105.5
```

Record 2:

```text
Systolic: 130
Diastolic: 84
Glucose: 114.5
```

Expected summary:

```text
Average systolic = 125.0
Average diastolic = 82.0
Average glucose = 110.0
Total records = 2
```

## Application Architecture

```text
Client
  ↓
FastAPI Routes
  ↓
Pydantic Validation
  ↓
Service Layer
  ↓
SQLite Database
  ↓
JSON Response
```

The project separates routing, validation, database access, and business logic to keep the code organized and maintainable.

## AI Engineering Relevance

The same architecture can be extended into an AI or machine-learning backend:

```text
Client
  ↓
FastAPI
  ↓
Request Validation
  ↓
ML / AI Model
  ↓
Database
  ↓
JSON Response
```

This pattern is commonly useful for model-serving APIs, predictive analytics systems, RAG applications, LLM services, and healthcare AI prototypes.

## Learning Outcomes

This project demonstrates practical understanding of:

- REST API architecture
- GET and POST operations
- Request and response lifecycle
- Nested JSON payloads
- Pydantic validation
- Custom HTTP error handling
- Path and query parameters
- SQLite persistence
- SQL aggregation
- UTC timestamps
- Swagger documentation
- Automated API testing
- Integration testing
- Clean backend project organization
- Git and GitHub workflow

## Disclaimer

This application is an educational software engineering project. It should only be tested with synthetic or properly de-identified data and must not be considered a clinical system.
