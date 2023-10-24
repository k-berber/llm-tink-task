import requests
from app.utils import MessageInfo


base_url = " http://localhost:8080"


def test_docker_run():
    url = base_url + "/health"
    response = requests.get(url)
    assert(response.ok, True)

@pytest.mark.parametrize('message_info', ()
def test_1():

