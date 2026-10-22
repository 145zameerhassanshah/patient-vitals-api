import os
import tempfile
import pytest
from fastapi.testclient import TestClient

@pytest.fixture()
def client():
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as temp_db:
        db_path = temp_db.name

    os.environ["VITALS_DB_PATH"] = db_path

    from app.database import init_database
    from app.main import app

    init_database()

    with TestClient(app) as test_client:
        yield test_client

    os.environ.pop("VITALS_DB_PATH", None)
    try:
        os.remove(db_path)
    except FileNotFoundError:
        pass
