from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException, Query, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.database import init_database
from app.schemas import PatientSummary, VitalCreate, VitalRecord
from app.services import create_vital_record, get_patient_summary, get_patient_vitals

app = FastAPI(
    title="Patient Vitals API",
    description="REST API for validating, storing, retrieving, and summarizing synthetic patient vitals.",
    version="1.0.0",
)

@app.on_event("startup")
def startup_event() -> None:
    init_database()

def format_validation_error(error: dict) -> str:
    location = [str(item) for item in error.get("loc", []) if item != "body"]
    field = ".".join(location) if location else "request"
    message = error.get("msg", "Invalid value")
    if message.startswith("Value error, "):
        message = message.replace("Value error, ", "", 1)

    error_type = error.get("type", "")
    if error_type == "missing":
        return f"{field} is required"
    if "int_type" in error_type or "int_parsing" in error_type:
        return f"{field} must be an integer"
    if "float_type" in error_type or "float_parsing" in error_type:
        return f"{field} must be a number"
    if "string_type" in error_type:
        return f"{field} must be a string"
    return message

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "Bad Request",
            "details": [format_validation_error(error) for error in exc.errors()],
        },
    )

@app.get("/health")
def health_check() -> dict:
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

@app.post("/vitals", response_model=VitalRecord, status_code=status.HTTP_201_CREATED)
def submit_vitals(vital: VitalCreate) -> dict:
    return create_vital_record(vital)

@app.get("/patients/{patient_id}/vitals", response_model=list[VitalRecord])
def patient_vitals_history(
    patient_id: str,
    limit: int | None = Query(default=None, ge=1),
) -> list[dict]:
    return get_patient_vitals(patient_id, limit)

@app.get("/patients/{patient_id}/summary", response_model=PatientSummary)
def patient_vitals_summary(patient_id: str) -> dict:
    summary = get_patient_summary(patient_id)
    if summary is None:
        raise HTTPException(
            status_code=404,
            detail=f"No vitals found for patient '{patient_id}'.",
        )
    return summary
