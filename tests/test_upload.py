from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_upload_receipt_succeeds(tmp_path):
    # Create a small fake "image" payload
    fake_bytes = b"\xff\xd8\xff\xdbFAKEJPEGDATA\xff\xd9"
    files = {"file": ("test.jpg", fake_bytes, "image/jpeg")}

    r = client.post("/upload-receipt", files=files)
    assert r.status_code == 200
    body = r.json()

    assert body["filename"] == "test.jpg"
    assert body["saved_as"].endswith(".jpg")
    assert body["size_bytes"] == len(fake_bytes)
    assert body["content_type"] == "image/jpeg"
    assert body["path"].startswith("./uploads/")
