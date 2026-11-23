"""httpx must keep a path prefix on SPRUT_API_BASE when requesting /api/..."""

import httpx

from sprutmonitor_mcp.config import DEFAULT_API_BASE


def test_cloud_base_keeps_v3_prefix() -> None:
    with httpx.Client(base_url=DEFAULT_API_BASE) as client:
        url = str(client.build_request("GET", "/api/Access/login-jwt").url)
    assert url == "https://cloud.sprutmonitor.ru/v3/api/Access/login-jwt"


def test_local_server_base_prefix_is_kept() -> None:
    with httpx.Client(base_url="https://monitor.example/MonitorServer") as client:
        url = str(client.build_request("GET", "/api/Access/login-jwt").url)
    assert url == "https://monitor.example/MonitorServer/api/Access/login-jwt"
