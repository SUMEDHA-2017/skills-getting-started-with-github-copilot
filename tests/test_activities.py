"""Tests for the activities endpoints."""

import pytest
from fastapi.testclient import TestClient


class TestGetActivities:
    """Test suite for GET /activities endpoint."""
    
    def test_get_activities_returns_200(self, client):
        """Test that GET /activities returns a 200 status code."""
        response = client.get("/activities")
        assert response.status_code == 200
    
    def test_get_activities_returns_dict(self, client):
        """Test that GET /activities returns a dictionary."""
        response = client.get("/activities")
        data = response.json()
        assert isinstance(data, dict)
    
    def test_get_activities_contains_expected_activities(self, client):
        """Test that the response contains expected activities."""
        response = client.get("/activities")
        data = response.json()
        
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Basketball Team",
            "Tennis Club",
            "Drama Club",
            "Art Studio",
            "Debate Team",
            "Science Club"
        ]
        
        for activity in expected_activities:
            assert activity in data
    
    def test_get_activities_has_required_fields(self, client):
        """Test that each activity has the required fields."""
        response = client.get("/activities")
        data = response.json()
        
        required_fields = ["description", "schedule", "max_participants", "participants"]
        
        for activity_name, activity_data in data.items():
            for field in required_fields:
                assert field in activity_data


class TestSignupForActivity:
    """Test suite for POST /activities/{activity_name}/signup endpoint."""
    
    def test_signup_new_participant_returns_200(self, client, reset_activities):
        """Test successful signup returns 200 status code."""
        response = client.post(
            "/activities/Chess%20Club/signup",
            params={"email": "newstudent@mergington.edu"}
        )
        assert response.status_code == 200
    
    def test_signup_new_participant_adds_to_list(self, client, reset_activities):
        """Test that signup adds participant to the participants list."""
        email = "newstudent@mergington.edu"
        response = client.post(
            "/activities/Chess%20Club/signup",
            params={"email": email}
        )
        
        assert response.status_code == 200
        
        # Verify participant was added
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert email in activities_data["Chess Club"]["participants"]
    
    def test_signup_returns_success_message(self, client, reset_activities):
        """Test that successful signup returns a success message."""
        email = "newstudent@mergington.edu"
        response = client.post(
            "/activities/Chess%20Club/signup",
            params={"email": email}
        )
        
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert "Chess Club" in data["message"]
    
    def test_signup_duplicate_returns_400(self, client, reset_activities):
        """Test that signing up an already registered student returns 400."""
        # Try to signup someone already registered
        response = client.post(
            "/activities/Chess%20Club/signup",
            params={"email": "michael@mergington.edu"}
        )
        
        assert response.status_code == 400
    
    def test_signup_duplicate_returns_error_message(self, client, reset_activities):
        """Test that duplicate signup returns appropriate error message."""
        response = client.post(
            "/activities/Chess%20Club/signup",
            params={"email": "michael@mergington.edu"}
        )
        
        data = response.json()
        assert "detail" in data
        assert "already signed up" in data["detail"]
    
    def test_signup_invalid_activity_returns_404(self, client):
        """Test that signup for non-existent activity returns 404."""
        response = client.post(
            "/activities/NonexistentActivity/signup",
            params={"email": "student@mergington.edu"}
        )
        
        assert response.status_code == 404
    
    def test_signup_invalid_activity_returns_error_message(self, client):
        """Test that signup for invalid activity returns error message."""
        response = client.post(
            "/activities/NonexistentActivity/signup",
            params={"email": "student@mergington.edu"}
        )
        
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()


class TestUnregisterFromActivity:
    """Test suite for DELETE /activities/{activity_name}/unregister endpoint."""
    
    def test_unregister_existing_participant_returns_200(self, client, reset_activities):
        """Test that unregistering an existing participant returns 200."""
        response = client.delete(
            "/activities/Chess%20Club/unregister",
            params={"email": "michael@mergington.edu"}
        )
        
        assert response.status_code == 200
    
    def test_unregister_removes_participant(self, client, reset_activities):
        """Test that unregister removes participant from the list."""
        email = "michael@mergington.edu"
        
        # Verify participant exists
        activities_response = client.get("/activities")
        assert email in activities_response.json()["Chess Club"]["participants"]
        
        # Unregister
        client.delete(
            "/activities/Chess%20Club/unregister",
            params={"email": email}
        )
        
        # Verify participant was removed
        activities_response = client.get("/activities")
        assert email not in activities_response.json()["Chess Club"]["participants"]
    
    def test_unregister_returns_success_message(self, client, reset_activities):
        """Test that successful unregister returns a success message."""
        email = "michael@mergington.edu"
        response = client.delete(
            "/activities/Chess%20Club/unregister",
            params={"email": email}
        )
        
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert "Chess Club" in data["message"]
    
    def test_unregister_non_registered_returns_400(self, client, reset_activities):
        """Test that unregistering a non-registered participant returns 400."""
        response = client.delete(
            "/activities/Chess%20Club/unregister",
            params={"email": "nonexistent@mergington.edu"}
        )
        
        assert response.status_code == 400
    
    def test_unregister_non_registered_returns_error_message(self, client, reset_activities):
        """Test that unregistering non-registered participant returns error message."""
        response = client.delete(
            "/activities/Chess%20Club/unregister",
            params={"email": "nonexistent@mergington.edu"}
        )
        
        data = response.json()
        assert "detail" in data
        assert "not registered" in data["detail"].lower()
    
    def test_unregister_invalid_activity_returns_404(self, client):
        """Test that unregister for non-existent activity returns 404."""
        response = client.delete(
            "/activities/NonexistentActivity/unregister",
            params={"email": "student@mergington.edu"}
        )
        
        assert response.status_code == 404
    
    def test_unregister_invalid_activity_returns_error_message(self, client):
        """Test that unregister for invalid activity returns error message."""
        response = client.delete(
            "/activities/NonexistentActivity/unregister",
            params={"email": "student@mergington.edu"}
        )
        
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()
