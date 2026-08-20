"""Typed API request/response models."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict

from .exceptions import PepkioAPIError


class CustomBufferInfo(BaseModel):
    """Custom buffer specification (pKa and molecular weights)."""

    model_config = ConfigDict(extra="allow")

    pka: float | None = None
    mw_acid: float | None = None
    mw_base: float | None = None
    name: str | None = None


class PHBufferSolverInput(BaseModel):
    """Input payload for ph-buffer-solver tool."""

    model_config = ConfigDict(extra="allow")

    tab: Literal["solver", "pka-reference", "history"] = "solver"
    solve_direction: Literal["forward", "reverse"] | str | None = None
    buffer_id: str | None = None
    target_ph: float | None = None
    total_concentration: float | None = None
    concentration_unit: Literal["M", "mM", "µM", "uM"] | str | None = None
    final_volume: float | None = None
    volume_unit: Literal["L", "mL", "µL", "uL"] | str | None = None
    temperature_c: float | None = None
    mole_ratio: float | None = None
    reagent_mode: Literal["solid_solid", "stock_stock", "titrant"] | str | None = None
    titrant: Literal["HCl", "NaOH"] | str | None = None
    custom_buffer: CustomBufferInfo | dict[str, Any] | None = None
    stock_acid_M: float | None = None
    stock_base_M: float | None = None
    titrant_stock_M: float | None = None


class RunOptions(BaseModel):
    """Optional fields for POST .../run."""

    idempotency_key: str | None = None
    label: str | None = None


class RunResult(BaseModel):
    """Tool run response envelope."""

    model_config = ConfigDict(extra="allow")

    run_id: str
    status: str
    result: dict[str, Any] | None = None
    error: dict[str, Any] | None = None
    result_url: str | None = None
    permalink: str | None = None
    duration_ms: int | None = None

    def raise_for_error(self) -> None:
        """Raise PepkioAPIError if the run response includes an error field."""
        if self.error is None:
            return
        err = self.error
        msg = err.get("message") if isinstance(err, dict) else str(err)
        code = err.get("code") if isinstance(err, dict) else None
        details = (
            err.get("details")
            if isinstance(err, dict) and isinstance(err.get("details"), dict)
            else {}
        )
        raise PepkioAPIError(
            msg or "Tool run failed",
            code=code,
            details=details,
            response_body={"run_id": self.run_id, "status": self.status, "error": self.error},
        )


def parse_run_response(data: dict[str, Any]) -> RunResult:
    """Parse a run API JSON body into RunResult."""
    return RunResult.model_validate(data)
