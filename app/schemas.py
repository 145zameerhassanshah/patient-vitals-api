from pydantic import BaseModel, ConfigDict, field_validator

class BloodPressure(BaseModel):
    model_config = ConfigDict(strict=True)
    systolic: int
    diastolic: int

    @field_validator("systolic")
    @classmethod
    def validate_systolic(cls, value: int) -> int:
        if not 50 <= value <= 300:
            raise ValueError("blood_pressure.systolic must be between 50 and 300")
        return value

    @field_validator("diastolic")
    @classmethod
    def validate_diastolic(cls, value: int) -> int:
        if not 30 <= value <= 200:
            raise ValueError("blood_pressure.diastolic must be between 30 and 200")
        return value

class VitalCreate(BaseModel):
    model_config = ConfigDict(strict=True)
    patient_id: str
    age: int
    blood_pressure: BloodPressure
    glucose_level: float | int

    @field_validator("patient_id")
    @classmethod
    def validate_patient_id(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("patient_id must not be empty")
        return cleaned

    @field_validator("age")
    @classmethod
    def validate_age(cls, value: int) -> int:
        if not 0 <= value <= 120:
            raise ValueError("age must be an integer between 0 and 120")
        return value

    @field_validator("glucose_level")
    @classmethod
    def validate_glucose(cls, value: float | int) -> float:
        value = float(value)
        if value <= 0:
            raise ValueError("glucose_level must be greater than 0")
        return value

class VitalRecord(BaseModel):
    id: int
    patient_id: str
    age: int
    blood_pressure: BloodPressure
    glucose_level: float
    recorded_at: str

class PatientSummary(BaseModel):
    patient_id: str
    average_systolic: float
    average_diastolic: float
    average_glucose: float
    total_records: int
