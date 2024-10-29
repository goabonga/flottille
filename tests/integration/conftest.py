from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def docker_compose_file():
    return str(Path(__file__).parent / "../../docker-compose.yaml")

@pytest.fixture(scope='session', autouse=True)
def clean_up_all_services(docker_services):
    yield
    docker_services._docker_compose.execute("down -v")