from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from api import app

client = TestClient(app)

def test_analyze_endpoint_queues_task():
    # Mockujemy pika, żeby nie potrzebować prawdziwego Rabbita do testu jednostkowego/integracyjnego API
    with patch("api.pika.BlockingConnection") as mock_conn:
        mock_channel = MagicMock()
        mock_conn.return_value.channel.return_value = mock_channel
        
        response = client.post("/analyze_img/", json={"url": "http://test.com/img.jpg"})
        
        assert response.status_code == 200
        data = response.json()
        assert "job_id" in data
        assert data["status"] == "queued"
        
        # Sprawdzamy czy API faktycznie wysłało coś do kolejki
        mock_channel.basic_publish.assert_called_once()