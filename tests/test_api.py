VALID_VITALS = {
    "patient_id": "P001",
    "age": 45,
    "blood_pressure": {"systolic": 120, "diastolic": 80},
    "glucose_level": 105.5,
}

def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert "timestamp" in body

def test_submit_valid_vitals(client):
    response = client.post("/vitals", json=VALID_VITALS)
    assert response.status_code == 201
    assert response.json()["patient_id"] == "P001"

def test_history_and_limit(client):
    client.post("/vitals", json=VALID_VITALS)
    client.post("/vitals", json={
        **VALID_VITALS,
        "blood_pressure": {"systolic": 130, "diastolic": 84},
        "glucose_level": 114.5,
    })
    all_response = client.get("/patients/P001/vitals")
    limited_response = client.get("/patients/P001/vitals?limit=1")
    assert all_response.status_code == 200
    assert len(all_response.json()) == 2
    assert limited_response.status_code == 200
    assert len(limited_response.json()) == 1

def test_summary(client):
    client.post("/vitals", json=VALID_VITALS)
    client.post("/vitals", json={
        **VALID_VITALS,
        "blood_pressure": {"systolic": 130, "diastolic": 84},
        "glucose_level": 114.5,
    })
    response = client.get("/patients/P001/summary")
    assert response.status_code == 200
    body = response.json()
    assert body["average_systolic"] == 125.0
    assert body["average_diastolic"] == 82.0
    assert body["average_glucose"] == 110.0
    assert body["total_records"] == 2

def test_empty_patient_id_returns_400(client):
    response = client.post("/vitals", json={**VALID_VITALS, "patient_id": "   "})
    assert response.status_code == 400

def test_missing_patient_id_returns_400(client):
    payload = {
        "age": 45,
        "blood_pressure": {"systolic": 120, "diastolic": 80},
        "glucose_level": 105.5,
    }
    response = client.post("/vitals", json=payload)
    assert response.status_code == 400

def test_age_out_of_range_returns_400(client):
    response = client.post("/vitals", json={**VALID_VITALS, "age": 121})
    assert response.status_code == 400

def test_systolic_out_of_range_returns_400(client):
    payload = {
        **VALID_VITALS,
        "blood_pressure": {"systolic": 301, "diastolic": 80},
    }
    assert client.post("/vitals", json=payload).status_code == 400

def test_diastolic_out_of_range_returns_400(client):
    payload = {
        **VALID_VITALS,
        "blood_pressure": {"systolic": 120, "diastolic": 29},
    }
    assert client.post("/vitals", json=payload).status_code == 400

def test_non_positive_glucose_returns_400(client):
    assert client.post("/vitals", json={**VALID_VITALS, "glucose_level": 0}).status_code == 400

def test_invalid_age_type_returns_400(client):
    assert client.post("/vitals", json={**VALID_VITALS, "age": "invalid"}).status_code == 400

def test_unknown_patient_summary_returns_404(client):
    assert client.get("/patients/UNKNOWN/summary").status_code == 404
