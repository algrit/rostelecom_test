import pytest


@pytest.fixture(scope="session", autouse=True)
def tasks_id():
    return []


@pytest.mark.parametrize(
    "device_id, params, status_code",
    [
        (
            "abcefg12",
            {
                "timeoutInSeconds": 0,
                "parameters": {
                    "username": "string",
                    "password": "string",
                    "interfaces": [1, 2, 3],
                },
            },
            200,
        ),
        (
            "abcefg12",
            {
                "timeoutInSeconds": 0,
                "parameters": {
                    "username": "string",
                    "password": "string",
                    "vlan": 12,
                    "interfaces": [1, 2, 3],
                },
            },
            200,
        ),
        (
            "abcefg12",
            {
                "timeoutInSeconds": 0,
                "ABRAKADABRA": {
                    "username": "string",
                    "password": "string",
                    "vlan": 0,
                    "interfaces": [1, 2, 3],
                },
            },
            422,
        ),
        (
            "123",
            {
                "timeoutInSeconds": 0,
                "parameters": {
                    "username": "string",
                    "password": "string",
                    "vlan": 0,
                    "interfaces": [1, 2, 3],
                },
            },
            404,
        ),
    ],
)
async def test_params_input(ac, device_id, params, status_code, tasks_id):
    response = await ac.post(f"/api/v1/equipment/cpe/{device_id}", json=params)
    assert response.status_code == status_code
    if status_code == 200:
        tasks_id.append(response.json()["task_id"])


@pytest.mark.parametrize(
    "device_id, task_id, status_code",
    [
        ("abcefg12", 0, 200),
        ("abcefg12", 1, 200),
    ],
)
async def test_params_check(ac, device_id, task_id, status_code, tasks_id):
    response = await ac.get(
        f"/api/v1/equipment/cpe/{device_id}/task/{tasks_id[task_id]}"
    )
    assert response.status_code == status_code
