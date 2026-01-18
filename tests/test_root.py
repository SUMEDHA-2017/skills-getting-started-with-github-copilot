"""Tests for the root endpoint."""

import pytest
from fastapi.testclient import TestClient


class TestRoot:
    """Test suite for the root endpoint."""
    
    def test_root_returns_redirect(self, client):
        """Test that GET / redirects to /static/index.html."""
        response = client.get("/", follow_redirects=False)
        
        # FastAPI redirects with status code 307
        assert response.status_code == 307
    
    def test_root_redirects_to_static_index(self, client):
        """Test that root endpoint redirects to static/index.html."""
        response = client.get("/", follow_redirects=False)
        
        assert "location" in response.headers
        assert "/static/index.html" in response.headers["location"]
