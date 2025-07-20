# Import pytest for writing and running tests
import pytest

# Import the Flask app instance from the main app file
from app import app

@pytest.fixture
def client():
    """A test client for the app."""
    # Create a test client using the Flask application configured for testing
    with app.test_client() as client:
        yield client # This is where the testing happens!

def test_home(client):
    """Test the home route."""
    response = client.get('/')
    assert response.status_code == 200
    assert response.json == {"message": "Hello, Flask!"}

def test_non_existent_route(client):
    """Test for a non-existent route."""
    response = client.get('/non-existent')
    assert response.status_code == 404

def test_get_all_securities(client):
    """Test the get_all_securities route."""
    response = client.get('/get-all-securities')
    assert response.status_code == 200
    assert response.json == {"message": "All securities retrieved successfully."}