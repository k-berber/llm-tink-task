import requests


base_url = " http://localhost:8080"


def test_docker_run():
    url = base_url + "/health"
    response = requests.get(url)
    assert(response.ok, True)
