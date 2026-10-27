from io import BytesIO
import pytest
from PIL import Image
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def sample_jpeg():
    b=BytesIO()
    Image.new("RGB",(80,60),(220,220,220)).save(b,format="JPEG")
    return b.getvalue()
