import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch

from enxame.main import app

client = TestClient(app)


@pytest.fixture
def mock_run_command():
    with patch("enxame.dokku.run_command", new_callable=AsyncMock) as mock:
        yield mock


def test_create_app_success(mock_run_command):
    mock_run_command.return_value = AsyncMock()
    response = client.post("/apps", json={"name": "test-app"})
    assert response.status_code == 200
    assert response.json() == {"name": "test-app"}
    mock_run_command.assert_called_once_with("dokku --quiet apps:create test-app")


def test_create_app_invalid_name():
    response = client.post("/apps", json={"name": "Invalid Name"})
    assert response.status_code == 422


def test_list_apps_success(mock_run_command):
    mock_run_command.return_value.stdout = "app1\napp2\napp3"
    response = client.get("/apps")
    assert response.status_code == 200
    assert response.json() == {
        "items": [{"name": "app1"}, {"name": "app2"}, {"name": "app3"}],
        "n_items": 3,
    }


def test_get_app_success(mock_run_command):
    mock_run_command.return_value.stdout = '{"ENV_VAR": "value"}'
    response = client.get("/apps/test-app")
    assert response.status_code == 200
    assert response.json() == {"name": "test-app", "config": {"ENV_VAR": "value"}}


def test_delete_app_success(mock_run_command):
    mock_run_command.return_value = AsyncMock()
    response = client.delete("/apps/test-app")
    assert response.status_code == 204
    mock_run_command.assert_called_once_with(
        "dokku --quiet apps:destroy --force test-app"
    )


def test_set_app_config_success(mock_run_command):
    mock_run_command.side_effect = [
        # clear config
        AsyncMock(),
        # set config
        AsyncMock(),
        # get updated config
        AsyncMock(stdout='{"NEW_VAR": "new_value"}'),
    ]
    response = client.put(
        "/apps/test-app/config", json={"config": {"NEW_VAR": "new_value"}}
    )
    assert response.status_code == 200
    assert response.json() == {"name": "test-app", "config": {"NEW_VAR": "new_value"}}


def test_set_app_config_empty(mock_run_command):
    mock_run_command.side_effect = [
        # clear config
        AsyncMock(),
        # get updated config
        AsyncMock(stdout="{}"),
    ]
    response = client.put("/apps/test-app/config", json={"config": {}})
    assert response.status_code == 200
    assert response.json() == {"name": "test-app", "config": {}}
