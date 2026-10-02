import io
import wave

from PIL import Image


def png_bytes():
    output = io.BytesIO()
    Image.new("RGB", (2, 2), (20, 200, 180)).save(output, "PNG")
    return output.getvalue()


def wav_bytes():
    output = io.BytesIO()
    with wave.open(output, "wb") as audio:
        audio.setnchannels(1)
        audio.setsampwidth(2)
        audio.setframerate(8000)
        audio.writeframes(b"\0\0" * 800)
    return output.getvalue()


def test_auth_lifecycle_and_revocation(client):
    registration = client.post("/api/auth/register", json={"email": "lifecycle@example.com", "full_name": "Lifecycle User", "password": "TestPass123!"})
    assert registration.status_code == 201
    token = registration.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    assert client.get("/api/auth/me", headers=headers).status_code == 200
    assert client.post("/api/auth/logout", headers=headers).status_code == 204
    assert client.get("/api/auth/me", headers=headers).status_code == 401
    assert client.post("/api/auth/login", json={"email": "lifecycle@example.com", "password": "TestPass123!"}).status_code == 200


def test_image_analysis_dashboard_history_and_pdf(authenticated_client):
    client, token = authenticated_client
    headers = {"Authorization": f"Bearer {token}"}
    upload = client.post("/api/media/upload", headers=headers, files={"file": ("sample.png", png_bytes(), "image/png")})
    assert upload.status_code == 201
    analysis = client.post("/api/analysis", headers=headers, json={"media_id": upload.json()["id"]})
    assert analysis.status_code == 201
    analysis_id = analysis.json()["id"]
    history = client.get("/api/analysis/history?page=1&page_size=1&media_type=image", headers=headers)
    assert history.status_code == 200
    assert history.json()["total"] == 1
    assert history.json()["items"][0]["id"] == analysis_id
    dashboard = client.get("/api/dashboard/stats", headers=headers)
    assert dashboard.status_code == 200
    assert dashboard.json()["average_confidence"] == analysis.json()["confidence"]
    report = client.post("/api/reports", headers=headers, json={"analysis_id": analysis_id, "title": "Test report", "format": "pdf"})
    assert report.status_code == 200
    report_detail = client.get(f"/api/reports/{report.json()['id']}", headers=headers)
    assert report_detail.status_code == 200
    assert report_detail.json()["analysis"]["media_name"] == "sample.png"
    pdf = client.get(f"/api/reports/{report.json()['id']}/download", headers=headers)
    assert pdf.status_code == 200
    assert pdf.headers["content-type"].startswith("application/pdf")
    assert pdf.content.startswith(b"%PDF-")
    assert client.delete(f"/api/analysis/{analysis_id}", headers=headers).status_code == 204


def test_media_validation(authenticated_client):
    client, token = authenticated_client
    headers = {"Authorization": f"Bearer {token}"}
    assert client.post("/api/media/upload", headers=headers, files={"file": ("empty.png", b"", "image/png")}).status_code == 400
    assert client.post("/api/media/upload", headers=headers, files={"file": ("fake.jpg", b"not-an-image", "image/jpeg")}).status_code == 415
    audio = client.post("/api/media/upload", headers=headers, files={"file": ("sample.wav", wav_bytes(), "audio/wav")})
    assert audio.status_code == 201
