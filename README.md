# Patient Vitals API

A professional FastAPI REST service for receiving, validating, storing, retrieving, and summarizing synthetic patient health metrics.

> Educational use only. This project is not a clinical diagnostic or treatment system.

## Features

- FastAPI REST endpoints
- SQLite persistence
- Pydantic validation
- Explicit HTTP 400 validation responses
- UTC timestamps
- Historical vitals retrieval
- Optional `limit` query parameter
- Average vitals summary
- Swagger docs
- Automated pytest tests

## Project Structure

```text
patient-vitals-api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── schemas.py
│   ├── database.py
│   └── services.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_api.py
├── .gitignore
├── pytest.ini
├── README.md
└── requirements.txt
```

## Setup

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run

```powershell
uvicorn app.main:app --reload
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

## Endpoints

### GET /health
Returns `"ok"` and the current UTC timestamp.

### POST /vitals

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

Successful submission returns `201 Created`.

### GET /patients/{patient_id}/vitals

```text
GET /patients/P001/vitals
```

Optional limit:

```text
GET /patients/P001/vitals?limit=2
```

### GET /patients/{patient_id}/summary

Returns average systolic, diastolic, glucose, and total record count.

## Validation

Invalid payloads return `400 Bad Request`.

Rules:

- `patient_id`: required and nonblank
- `age`: integer from 0 to 120
- `systolic`: 50 to 300
- `diastolic`: 30 to 200
- `glucose_level`: greater than 0

## Automated Tests

```powershell
pytest
```

Tests cover valid submissions, history retrieval, limit behavior, summary calculations, missing/blank IDs, out-of-range values, invalid data types, and unknown-patient summaries.

## curl Examples

```bash
curl http://127.0.0.1:8000/health
```

```bash
curl -X POST http://127.0.0.1:8000/vitals -H "Content-Type: application/json" -d "{\"patient_id\":\"P001\",\"age\":45,\"blood_pressure\":{\"systolic\":120,\"diastolic\":80},\"glucose_level\":105.5}"
```

```bash
curl http://127.0.0.1:8000/patients/P001/vitals
```

```bash
curl http://127.0.0.1:8000/patients/P001/summary
```

## AI Engineering Relevance

The same backend pattern can sit in front of an ML model:

```text
Client → FastAPI → Validation → ML Model → Database → JSON Response
```

This makes the project a useful foundation for model-serving and healthcare analytics APIs.
