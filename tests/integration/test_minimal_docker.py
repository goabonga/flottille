import httpx

def test_minimal_container(docker_services, docker_ip):
    # Define the service name and port as per your docker-compose configuration
    service_name = "backend"
    service_port = 8080  # Update this to match your docker-compose.yml

    # Retrieve the external port mapped to the service's internal port
    port = docker_services.port_for(service_name, service_port)
    url = f"http://{docker_ip}:{port}"

    # Increase the wait time to give the container more time to start up
    docker_services.wait_until_responsive(
        timeout=60.0,  # Extended timeout to 60 seconds
        pause=0.5,     # Check every 0.5 seconds
        check=lambda: is_service_responsive(url)
    )

    # Perform the test request with httpx
    response = httpx.get(f"{url}/heartbeat")
    assert response.status_code == 200

def is_service_responsive(url):
    try:
        response = httpx.get(url, timeout=5.0)
        return response.status_code == 404
    except httpx.RequestError:
        return False
