"""
Extended destination metadata for UI 2 — AI Crowd Redistribution Engine.

Separate from UI 1's destinations.json / data_generator.py.
Used for similarity matching and geographic proximity scoring.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path

METADATA_PATH = Path(__file__).parent / "data" / "destination_metadata.json"

VALID_CATEGORIES = frozenset({
    "heritage",
    "beach",
    "hill-station",
    "wildlife",
    "religious",
})

VALID_IDEAL_FOR = frozenset({"family", "couple", "solo", "adventure"})


@dataclass(frozen=True)
class DestinationMetadata:
    destination_id: str
    name: str
    city: str
    state: str
    category: str
    tags: tuple[str, ...]
    latitude: float
    longitude: float
    average_visit_duration_hours: float
    ideal_for: tuple[str, ...]

    @property
    def tag_text(self) -> str:
        """Space-joined tags + category for TF-IDF similarity."""
        return " ".join([self.category, *self.tags])


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance between two lat/lon points in kilometres."""
    r = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = (
        math.sin(dphi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    )
    return r * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def load_destination_metadata(
    path: Path | None = None,
) -> dict[str, DestinationMetadata]:
    """Load extended metadata keyed by destination_id."""
    src = path or METADATA_PATH
    with open(src, encoding="utf-8") as f:
        raw = json.load(f)

    result: dict[str, DestinationMetadata] = {}
    for item in raw:
        meta = DestinationMetadata(
            destination_id=item["destination_id"],
            name=item["name"],
            city=item["city"],
            state=item["state"],
            category=item["category"],
            tags=tuple(item["tags"]),
            latitude=float(item["latitude"]),
            longitude=float(item["longitude"]),
            average_visit_duration_hours=float(item["average_visit_duration_hours"]),
            ideal_for=tuple(item["ideal_for"]),
        )
        result[meta.destination_id] = meta
    return result


def get_metadata_or_raise(
    destination_id: str,
    catalog: dict[str, DestinationMetadata] | None = None,
) -> DestinationMetadata:
    catalog = catalog or load_destination_metadata()
    if destination_id not in catalog:
        raise ValueError(f"Unknown destination_id for recommendations: {destination_id}")
    return catalog[destination_id]
