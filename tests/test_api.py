import requests

from app.api.api_v1.endpoints import html
from app.config import settings

BASE_URL = settings.TEST_BASE_URL

headers = {
    "Authorization": f"Bearer {settings.API_KEYS[0]}",
    "Content-Type": "application/json",
}


def create_api_endpoint(path):
    return f"{BASE_URL}/{path}"


def test_api_v1_endpoint_root():
    r = requests.get(BASE_URL)
    assert r.status_code == 200
    assert r.text == html.html


def test_api_v1_endpoint_staticfiles():
    staticfiles = [p.name for p in settings.STATIC_PATH.iterdir()]
    r = requests.get(create_api_endpoint("f"))
    assert r.status_code == 200
    assert sorted(r.json()) == sorted(staticfiles)

    for file in staticfiles:
        assert (settings.STATIC_PATH / file).exists()


def test_api_v1_endpoint_monitoring():
    ping_url = create_api_endpoint("ping")
    assert requests.get(ping_url).status_code == 200

    health_url = create_api_endpoint("health")
    assert requests.get(health_url).json() == {"status": "ok"}

    protected_url = create_api_endpoint("protected")
    assert requests.get(protected_url).status_code == 401
    assert requests.get(protected_url, headers=headers).status_code == 200


def test_api_v1_endpoint_llm_tags():
    tagit_url = create_api_endpoint("llm/tagit")
    assert requests.post(tagit_url, json={"content": "test"}).status_code == 401

    r = requests.post(tagit_url, json={"content": "test"}, headers=headers)
    assert r.status_code == 200
    assert "#" in r.text

    tag_memo_url = create_api_endpoint("llm/memo_with_tag")
    r = requests.post(tag_memo_url, json={"content": "test"}, headers=headers)
    assert r.status_code == 200


def test_api_v1_endpoint_llm_edit():
    editit_url = create_api_endpoint("llm/editit")
    assert requests.post(editit_url, json={"content": "test"}).status_code == 401

    r = requests.post(editit_url, json={"content": "test"}, headers=headers)
    assert r.status_code == 200
    assert r.text

    fix_memo_url = create_api_endpoint("llm/memo_with_fix")
    r = requests.post(
        fix_memo_url, json={"content": "you creates a api"}, headers=headers
    )
    r = requests.post(fix_memo_url, json={"content": "他今天没有出门。"}, headers=headers)
    assert r.status_code == 200
