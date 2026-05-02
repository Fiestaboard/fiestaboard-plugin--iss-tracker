"""Display the real-time position and altitude of the International Space Station."""

from __future__ import annotations

import logging
from typing import Any, Dict, List
import requests

from src.plugins.base import PluginBase, PluginResult

logger = logging.getLogger(__name__)

API_URL = "https://api.wheretheiss.at/v1/satellites/25544"
USER_AGENT = "FiestaBoard ISS Tracker Plugin (https://github.com/Fiestaboard/fiestaboard-plugin--iss-tracker)"


class IssTrackerPlugin(PluginBase):
    """ISS Tracker plugin for FiestaBoard."""

    @property
    def plugin_id(self) -> str:
        return "iss_tracker"

    def fetch_data(self) -> PluginResult:
        try:
            response = requests.get(
                API_URL,
                headers={"User-Agent": USER_AGENT},
                timeout=10,
            )
            response.raise_for_status()
            d = response.json()

            return PluginResult(
                available=True,
                data={
                    "latitude": round(float(d["latitude"]), 2),
                    "longitude": round(float(d["longitude"]), 2),
                    "altitude_km": round(float(d["altitude"]), 1),
                    "velocity_kph": round(float(d["velocity"]), 0),
                    "visibility": str(d.get("visibility", "unknown")),
                },
            )
        except Exception as e:
            logger.exception("Error fetching ISS position")
            return PluginResult(available=False, error=str(e))

    def validate_config(self, config: Dict[str, Any]) -> List[str]:
        return []

    def cleanup(self) -> None:
        pass
