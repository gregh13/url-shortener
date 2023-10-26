from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_api():
    res_home = client.get("/")

    res_no_params = client.post(url="/api/shorten_url", json={})

    res_params1 = client.post(url="/api/shorten_url",
                              json={"original_url": "http://www.original.com"})

    res_params2 = client.post(url="/api/shorten_url",
                              json={"original_url": "http://www.original.com",
                                    "custom_url": "thegoods"})

    results = [res_home, res_no_params, res_params1, res_params2]
    for r in results:
        print(r.json())


test_api()
