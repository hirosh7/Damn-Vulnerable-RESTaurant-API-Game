def test_healthcheck(anon_client):
    response = anon_client.get("/healthcheck")
    assert response.status_code == 200
    assert response.json().get("ok") is True


def test_healthcheck_no_tech_stack_disclosure(anon_client):
    """
    Verify that the healthcheck endpoint does not expose technology stack
    information via X-Powered-By or similar headers (security requirement).
    """
    response = anon_client.get("/healthcheck")
    assert response.status_code == 200
    
    # Verify no X-Powered-By header is present
    assert "X-Powered-By" not in response.headers, \
        "X-Powered-By header should not be present (information disclosure)"
    
    # Verify no Server header with detailed info (if present, should be generic)
    if "Server" in response.headers:
        server_header = response.headers["Server"].lower()
        assert "python" not in server_header, \
            "Server header should not expose Python version"
        assert "fastapi" not in server_header, \
            "Server header should not expose FastAPI version"
