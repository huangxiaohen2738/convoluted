import requests


def mock_requests(monkeypatch, method="get", response=None, code=200):
    """
    :param monkeypatch: monkeypatch
    :param response: requests json response
    :param code: 200
    该方法主要用于 mock 使用 requests 请求外部接口:

        @pytest.fixture
        def mock_crm_api(monkeypatch, mock_user):
            mock_resp = {"users": [mock_user]}
            yield mock_requests(monkeypatch, response=mock_resp)

        @pytest.fixture
        def mock_crm_no_auth(monkeypatch):
            yield mock_requests(monkeypatch, method="post", code=401)

        def test_user(client, mock_crm_api):
            ...

        def test_user_no_auth(client, mock_crm_no_auth):
            ...
    """

    class MockRequests:

        def __init__(self, code, response):
            self.code = code
            self.response = response

        @property
        def ok(self):
            return int(self.code) == 200

        def json(self):
            return self.response

        def raise_for_status(self):
            if not self.ok:
                raise

        @property
        def status_code(self):
            return self.code

    def mock_call(mock_return_value):
        def mock(*args, **kwargs):
            return MockRequests(**mock_return_value)

        return mock

    return_value = {"code": code, "response": response or {}}
    monkeypatch.setattr(
        requests.Session, method.lower(),
        mock_call(return_value)
    )
