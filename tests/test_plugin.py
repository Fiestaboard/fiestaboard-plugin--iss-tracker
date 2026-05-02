"""Tests for the iss_tracker plugin."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch, Mock

import pytest

from plugins.iss_tracker import IssTrackerPlugin
from src.plugins.base import PluginResult

MANIFEST = json.loads("""
{
    "id": "iss_tracker",
    "name": "ISS Tracker",
    "version": "0.1.0",
    "settings_schema": {
        "type": "object",
        "properties": {
            "enabled": {
                "type": "boolean",
                "title": "Enabled",
                "default": false
            },
            "refresh_seconds": {
                "type": "integer",
                "title": "Refresh Interval (seconds)",
                "description": "How often to fetch ISS position.",
                "default": 60,
                "minimum": 30
            }
        },
        "required": []
    }
}
""")

SAMPLE_RESPONSE = json.loads("""
{
    "name": "iss",
    "id": 25544,
    "latitude": 51.5074,
    "longitude": -0.1278,
    "altitude": 408.32,
    "velocity": 27600.1,
    "visibility": "daylight",
    "footprint": 4535.4,
    "timestamp": 1700000000,
    "daynum": 2460000.5,
    "solar_lat": 12.3,
    "solar_lon": 100.5,
    "units": "kilometers"
}
""")


@pytest.fixture
def plugin():
    return IssTrackerPlugin(MANIFEST)


@pytest.fixture
def configured_plugin():
    p = IssTrackerPlugin(MANIFEST)
    p.config = json.loads("""
{}
""")
    return p


class TestIssTrackerPlugin:

    def test_plugin_id(self, plugin):
        assert plugin.plugin_id == "iss_tracker"

    def test_manifest_valid(self):
        manifest_path = Path(__file__).parent.parent / "manifest.json"
        with open(manifest_path) as f:
            m = json.load(f)
        for field in ("id", "name", "version"):
            assert field in m

    @patch("plugins.iss_tracker.requests.get")
    def test_fetch_data_success(self, mock_get, configured_plugin):
        mock_response = Mock()
        mock_response.json.return_value = SAMPLE_RESPONSE
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = configured_plugin.fetch_data()

        assert result.available is True
        assert result.error is None
        assert result.data is not None
        assert "latitude" in result.data, "missing variable: latitude"
        assert "longitude" in result.data, "missing variable: longitude"
        assert "altitude_km" in result.data, "missing variable: altitude_km"
        assert "velocity_kph" in result.data, "missing variable: velocity_kph"
        assert "visibility" in result.data, "missing variable: visibility"

    @patch("plugins.iss_tracker.requests.get")
    def test_fetch_data_network_error(self, mock_get, configured_plugin):
        import requests as req_mod
        mock_get.side_effect = req_mod.exceptions.ConnectionError("network down")

        result = configured_plugin.fetch_data()

        assert result.available is False
        assert result.error is not None

    @patch("plugins.iss_tracker.requests.get")
    def test_fetch_data_bad_json(self, mock_get, configured_plugin):
        mock_response = Mock()
        mock_response.json.side_effect = ValueError("bad json")
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = configured_plugin.fetch_data()

        assert result.available is False

