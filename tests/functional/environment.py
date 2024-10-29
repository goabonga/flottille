# environment.py
import os
import subprocess
import time
import subprocess
import httpx
import time

def wait_for_service(url, retries=5, delay=2):
    for _ in range(retries):
        try:
            response = httpx.get(url)
            if response.status_code == 200 or response.status_code == 404:
                print("Service is up!")
                return True
        except httpx.RequestError:
            pass
        time.sleep(delay)
    raise Exception("Service did not start in time.")

class APIContext:
    def __init__(self):
        self.response = None
        self.headers = {}
        self.base_url = ""


def before_all(context):
    """Lance les services Docker avant tous les tests."""
    print("Starting Docker services...")
    result = subprocess.run(['docker', 'compose', 'up', '-d'], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Failed to start Docker services: {result.stderr}")
        raise Exception("Docker services could not be started.")
    else:
        print(f"Docker services started successfully: {result.stdout}")
    
    context.api = APIContext()

    wait_for_service("http://127.0.0.1:8080/")
    


def after_all(context):
    """Hook executed after all tests are finished."""
    print("Stopping Docker services...")
    result = subprocess.run(['docker', 'compose', 'down', '--volume'], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Failed to stop Docker services: {result.stderr}")
    else:
        print(f"Docker services stopped successfully: {result.stdout}")
