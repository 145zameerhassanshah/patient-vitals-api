from datetime import datetime, timezone
from typing import Optional

from app.database import get_connection
from app.schemas import VitalCreate

def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def create_vital_record(vital: VitalCreate) -> dict:
    recorded_at = utc_now_iso()
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO vitals
            (patient_id, age, systolic, diastolic, glucose_level, recorded_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                vital.patient_id,
                vital.age,
                vital.blood_pressure.systolic,
                vital.blood_pressure.diastolic,
                float(vital.glucose_level),
                recorded_at,
            ),
        )
        record_id = cursor.lastrowid

    return {
        "id": record_id,
        "patient_id": vital.patient_id,
        "age": vital.age,
        "blood_pressure": {
            "systolic": vital.blood_pressure.systolic,
            "diastolic": vital.blood_pressure.diastolic,
        },
        "glucose_level": float(vital.glucose_level),
        "recorded_at": recorded_at,
    }

def get_patient_vitals(patient_id: str, limit: Optional[int] = None) -> list[dict]:
    query = """
        SELECT id, patient_id, age, systolic, diastolic, glucose_level, recorded_at
        FROM vitals
        WHERE patient_id = ?
        ORDER BY recorded_at DESC, id DESC
    """
    params = [patient_id]

    if limit is not None:
        query += " LIMIT ?"
        params.append(limit)

    with get_connection() as connection:
        rows = connection.execute(query, params).fetchall()

    return [
        {
            "id": row["id"],
            "patient_id": row["patient_id"],
            "age": row["age"],
            "blood_pressure": {
                "systolic": row["systolic"],
                "diastolic": row["diastolic"],
            },
            "glucose_level": row["glucose_level"],
            "recorded_at": row["recorded_at"],
        }
        for row in rows
    ]

def get_patient_summary(patient_id: str) -> dict | None:
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT
                AVG(systolic) AS average_systolic,
                AVG(diastolic) AS average_diastolic,
                AVG(glucose_level) AS average_glucose,
                COUNT(*) AS total_records
            FROM vitals
            WHERE patient_id = ?
            """,
            (patient_id,),
        ).fetchone()

    if row["total_records"] == 0:
        return None

    return {
        "patient_id": patient_id,
        "average_systolic": round(row["average_systolic"], 2),
        "average_diastolic": round(row["average_diastolic"], 2),
        "average_glucose": round(row["average_glucose"], 2),
        "total_records": row["total_records"],
    }
