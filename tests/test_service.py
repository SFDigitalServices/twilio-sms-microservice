# pylint: disable=redefined-outer-name
"""Tests for microservice"""
import json
import jsend
import pytest
from falcon import testing
import service.microservice
import tests.mocks as mocks
from service.resources.models import create_models
from service.resources.db import create_session


CLIENT_HEADERS = {
    "ACCESS_KEY": "1234567"
}

session = create_session() # pylint: disable=invalid-name
db = session() # pylint: disable=invalid-name

@pytest.fixture()
def client():
    """ client fixture """
    return testing.TestClient(app=service.microservice.start_service(), headers=CLIENT_HEADERS)

@pytest.fixture
def mock_env_access_key(monkeypatch):
    """ mock environment access key """
    monkeypatch.setenv("ACCESS_KEY", CLIENT_HEADERS["ACCESS_KEY"])

@pytest.fixture
def mock_env_no_access_key(monkeypatch):
    """ mock environment with no access key """
    monkeypatch.delenv("ACCESS_KEY", raising=False)

def test_welcome(client, mock_env_access_key):
    # pylint: disable=unused-argument
    # mock_env_access_key is a fixture and creates a false positive for pylint
    """Test welcome message response"""
    response = client.simulate_get('/welcome')
    assert response.status_code == 200

    expected_msg = jsend.success({'message': 'Welcome'})
    assert json.loads(response.content) == expected_msg

    # Test welcome request with no ACCESS_KEY in header
    client_no_access_key = testing.TestClient(service.microservice.start_service())
    response = client_no_access_key.simulate_get('/welcome')
    assert response.status_code == 403

def test_welcome_no_access_key(client, mock_env_no_access_key):
    # pylint: disable=unused-argument
    # mock_env_no_access_key is a fixture and creates a false positive for pylint
    """Test welcome request with no ACCESS_key environment var set"""
    response = client.simulate_get('/welcome')
    assert response.status_code == 403

def test_default_error(client, mock_env_access_key):
    # pylint: disable=unused-argument
    """Test default error response"""
    response = client.simulate_get('/some_page_that_does_not_exist')

    assert response.status_code == 404

def test_submission(mock_env_access_key, client):
    # pylint: disable=unused-argument
    """Test submission"""
    response = client.simulate_post(
        '/submission/testtable',
        json=mocks.SUBMISSION_POST_DATA
    )
    assert response.status_code == 200
    response_json = json.loads(response.text)
    assert response_json["status"] == "success"

    # check that its in the db
    submission_id = response_json["data"]["submission_id"]
    SubmissionModel = create_models('testtable')
    _s = db.query(SubmissionModel).filter(SubmissionModel.id == submission_id) # pylint: disable=E1101
    assert _s is not None

    # delete test data
    db.query(SubmissionModel).filter(SubmissionModel.id == submission_id).delete() # pylint: disable=E1101
    db.commit() # pylint: disable=E1101

    # no submission data
    response = client.simulate_post(
        '/submission/testtable',
        json={}
    )
    assert response.status_code == 500
    # fail db insert
    response = client.simulate_post(
        '/submission/testtable123',
        json=mocks.SUBMISSION_POST_DATA
    )
    assert response.status_code == 500
