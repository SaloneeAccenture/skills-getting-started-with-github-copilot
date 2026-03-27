"""
Test suite for Mergington High School Activities API

Tests use the AAA (Arrange-Act-Assert) pattern:
- Arrange: Set up test data and preconditions
- Act: Execute the action being tested
- Assert: Verify the results
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app


# Create a test client for the FastAPI app
client = TestClient(app)


class TestSignup:
    """Tests for the POST /activities/{activity_name}/signup endpoint"""

    def test_signup_success(self):
        """
        Test: A student can successfully sign up for an activity
        Arrange: Prepare activity name and email
        Act: Send POST request to signup endpoint
        Assert: Response has 200 status and success message
        """
        # Arrange
        activity = "Chess Club"
        email = "newstudent@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity}/signup?email={email}"
        )

        # Assert
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]
        assert email in response.json()["message"]

    def test_signup_nonexistent_activity(self):
        """
        Test: Signing up for a non-existent activity returns 404
        Arrange: Prepare a non-existent activity name and email
        Act: Send POST request to signup endpoint
        Assert: Response has 404 status and error detail
        """
        # Arrange
        activity = "Nonexistent Activity"
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity}/signup?email={email}"
        )

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_signup_duplicate(self):
        """
        Test: Signing up twice for the same activity returns 400
        Arrange: Use a student already signed up (emma@mergington.edu for Programming Class)
        Act: Send POST request to signup endpoint with duplicate email
        Assert: Response has 400 status and duplicate error message
        """
        # Arrange
        activity = "Programming Class"
        email = "emma@mergington.edu"  # Already signed up

        # Act
        response = client.post(
            f"/activities/{activity}/signup?email={email}"
        )

        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Student already signed up for this activity"


class TestUnregister:
    """Tests for the DELETE /activities/{activity_name}/unregister endpoint"""

    def test_unregister_success(self):
        """
        Test: A student can successfully unregister from an activity
        Arrange: Use a student already signed up (michael@mergington.edu for Chess Club)
        Act: Send DELETE request to unregister endpoint
        Assert: Response has 200 status and success message
        """
        # Arrange
        activity = "Chess Club"
        email = "michael@mergington.edu"  # Already signed up

        # Act
        response = client.delete(
            f"/activities/{activity}/unregister?email={email}"
        )

        # Assert
        assert response.status_code == 200
        assert "Unregistered" in response.json()["message"]
        assert email in response.json()["message"]

    def test_unregister_nonexistent_activity(self):
        """
        Test: Unregistering from a non-existent activity returns 404
        Arrange: Prepare a non-existent activity name and email
        Act: Send DELETE request to unregister endpoint
        Assert: Response has 404 status and error detail
        """
        # Arrange
        activity = "Nonexistent Activity"
        email = "student@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity}/unregister?email={email}"
        )

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_unregister_not_signed_up(self):
        """
        Test: Unregistering a student not signed up returns 400
        Arrange: Use a student not signed up (e.g., new email with Basketball Team)
        Act: Send DELETE request to unregister endpoint
        Assert: Response has 400 status and not signed up error message
        """
        # Arrange
        activity = "Basketball Team"
        email = "notstudent@mergington.edu"  # Not signed up

        # Act
        response = client.delete(
            f"/activities/{activity}/unregister?email={email}"
        )

        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Student is not signed up for this activity"
