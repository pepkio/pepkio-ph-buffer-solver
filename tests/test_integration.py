"""Integration tests against live Pepkio Tools API."""

from __future__ import annotations

import os
from pathlib import Path

import pytest
from dotenv import load_dotenv

from pepkio_ph_buffer_solver.client import PepkioClient

# Search upwards for .env if present
env_file = Path(__file__).resolve().parents[3] / ".env"
if env_file.exists():
    load_dotenv(env_file)
else:
    load_dotenv()

ENVIRONMENTS = [
    ("local", "https://tools.localtest.me"),
    ("production", "https://tools.pepkio.com"),
]


def _api_key_for(base_url: str) -> str | None:
    if "localtest.me" in base_url:
        return os.getenv("LOCAL_PEPKIO_API_KEY")
    return os.getenv("PEPKIO_API_KEY")


@pytest.fixture(params=ENVIRONMENTS, ids=["local", "production"])
def live_client(request):
    env_name, base_url = request.param
    api_key = _api_key_for(base_url)
    if not api_key:
        pytest.skip(f"No API key for {env_name} (set LOCAL_PEPKIO_API_KEY or PEPKIO_API_KEY)")
    with PepkioClient(api_key=api_key, base_url=base_url) as client:
        yield client


def test_get_manifest(live_client: PepkioClient):
    manifest = live_client.get_manifest(refresh=True)
    assert manifest["tool_id"] == "ph-buffer-solver"
    names = live_client.list_examples()
    assert "phosphate_50mM_pH74" in names


def test_run_phosphate_example(live_client: PepkioClient):
    inp = live_client.get_example_input("phosphate_50mM_pH74")
    result = live_client.run(inp)
    assert result.status == "completed"
    assert result.run_id
    assert result.permalink
    assert result.result is not None
    assert result.error is None


def test_run_tris_example(live_client: PepkioClient):
    inp = live_client.get_example_input("tris_forward_ratio")
    result = live_client.run(inp)
    assert result.status == "completed"
    assert result.result is not None


def test_run_pka_library_example(live_client: PepkioClient):
    inp = live_client.get_example_input("pka_library")
    result = live_client.run(inp)
    assert result.status == "completed"
    assert result.result is not None


def test_get_run_after_run(live_client: PepkioClient):
    inp = live_client.get_example_input("phosphate_50mM_pH74")
    run1 = live_client.run(inp)
    assert run1.run_id

    run2 = live_client.get_run(run1.run_id)
    assert run2.run_id == run1.run_id
    assert run2.status == "completed"
    assert run2.result is not None
