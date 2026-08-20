"""Test fixtures for unit tests."""

from __future__ import annotations

import pytest


@pytest.fixture
def mock_manifest():
    return {
        "schema_version": "1.0",
        "tool_id": "ph-buffer-solver",
        "title": "pH Buffer Solver",
        "description": "Henderson–Hasselbalch buffer solver",
        "execution_mode": "sync",
        "input": {
            "type": "object",
            "required": ["tab"],
            "properties": {
                "tab": {"type": "string"},
                "solve_direction": {"type": "string"},
                "buffer_id": {"type": "string"},
            },
        },
        "examples": [
            {
                "name": "phosphate_50mM_pH74",
                "input": {
                    "tab": "solver",
                    "solve_direction": "reverse",
                    "buffer_id": "phosphate",
                    "target_ph": 7.4,
                    "total_concentration": 50,
                    "concentration_unit": "mM",
                    "final_volume": 100,
                    "volume_unit": "mL",
                    "temperature_c": 25,
                    "reagent_mode": "solid_solid",
                },
                "output": {"solver": {"target_ph": 7.4, "buffer_capacity_mM_per_pH": 19.2}},
            },
            {
                "name": "tris_forward_ratio",
                "input": {
                    "tab": "solver",
                    "solve_direction": "forward",
                    "buffer_id": "tris",
                    "mole_ratio": 0.5,
                    "total_concentration": 50,
                    "concentration_unit": "mM",
                    "final_volume": 100,
                    "volume_unit": "mL",
                    "temperature_c": 25,
                    "reagent_mode": "solid_solid",
                },
                "output": {"solver": {"ph": 7.77}},
            },
            {
                "name": "pka_library",
                "input": {"tab": "pka-reference"},
                "output": {"library": {"buffers": [{"id": "tris"}]}},
            },
        ],
    }


@pytest.fixture
def mock_run_response():
    return {
        "run_id": "run_test123",
        "status": "completed",
        "result": {
            "tab": "solver",
            "warnings": [],
            "solver": {
                "solve_direction": "reverse",
                "buffer_label": "Sodium phosphate",
                "pKa_effective": 7.2,
                "target_ph": 7.4,
            },
        },
        "error": None,
        "result_url": "https://tools.pepkio.com/api/tools/v1/runs/run_test123",
        "permalink": "https://tools.pepkio.com/r/run_test123",
    }
