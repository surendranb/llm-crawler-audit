# SPDX-License-Identifier: MIT
"""Unit tests for telemetry Schema v2 and privacy compliance."""
import os
from unittest.mock import patch

from llm_crawler_audit.telemetry import (
    scrub_props,
    _telemetry_disabled,
    track_tool_call,
    track_event,
)


def test_telemetry_disabled(monkeypatch):
    monkeypatch.setenv("DO_NOT_TRACK", "1")
    assert _telemetry_disabled() is True

    monkeypatch.delenv("DO_NOT_TRACK", raising=False)
    monkeypatch.setenv("MCP_TELEMETRY_OPT_OUT", "true")
    assert _telemetry_disabled() is True


def test_scrub_props_redaction():
    payload = {
        "api_key": "sk-1234567890abcdef",
        "secret_token": "my-secret-token",
        "normal_key": "safe_value",
        "long_text": "x" * 500,
    }
    clean = scrub_props(payload)
    assert clean["api_key"] == "[REDACTED]"
    assert clean["secret_token"] == "[REDACTED]"
    assert clean["normal_key"] == "safe_value"
    assert len(clean["long_text"]) <= 300


def test_track_tool_call_safe(monkeypatch):
    monkeypatch.setenv("MCP_TELEMETRY_OPT_OUT", "1")
    # Should be a no-op and never raise
    track_tool_call("doctor", 12.5, "success")
    track_event("test_event", {"foo": "bar"})
