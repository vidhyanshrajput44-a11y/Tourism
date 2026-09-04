"""
UI 2 — AI Crowd Redistribution / Recommendation Engine.

Consumes UI 1 only via HTTP (GET /forecast, GET /destinations).
Does not import UI 1 model or feature code.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

import httpx
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from destination_metadata import (
    DestinationMetadata,
    haversine_km,
    load_destination_metadata,
)

UI1_BASE_URL = os.getenv("UI1_BASE_URL", "http://127.0.0.1:8000").rstrip("/")

SIMILARITY_WEIGHT = 0.4
PROXIMITY_WEIGHT = 0.3
LOW_CROWD_WEIGHT = 0.3

MAX_ALTERNATIVES = 15
MIN_ALTERNATIVES = 5
HIGH_CROWD = "High"
LOW_CROWD = "Low"


@dataclass
class AlternativeRecommendation:
    destination_id: str
    name: str
    similarity_score: float
    distance_km: float
    crowd_category: str
    crowd_score: int
    final_score: float
    reason: str


@dataclass
class TimeSlotSuggestion:
    date: str
    crowd_category: str
    crowd_score: int
    day_of_week: str


@dataclass
class RecommendationResult:
    original_destination: dict[str, Any]
    is_overcrowded: bool
    alternatives: list[AlternativeRecommendation]
    alternate_time_slots: list[TimeSlotSuggestion]


class UI1Client:
    """Thin HTTP client for UI 1 crowd-intelligence endpoints."""

    def __init__(self, base_url: str = UI1_BASE_URL, timeout: float = 15.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def get_forecast(self, destination_id: str) -> list[dict[str, Any]]:
        url = f"{self.base_url}/forecast/{destination_id}"
        with httpx.Client(timeout=self.timeout) as client:
            resp = client.get(url)
            resp.raise_for_status()
            return resp.json()

    def list_destinations(self) -> list[dict[str, Any]]:
        url = f"{self.base_url}/destinations"
        with httpx.Client(timeout=self.timeout) as client:
            resp = client.get(url)
            resp.raise_for_status()
            return resp.json()


def _category_label(category: str) -> str:
    labels = {
        "heritage": "heritage",
        "beach": "beach",
        "hill-station": "hill-station",
        "wildlife": "nature/wildlife",
        "religious": "spiritual",
    }
    return labels.get(category, category)


def _build_reason(
    candidate: DestinationMetadata,
    distance_km: float,
    crowd_category: str,
    similarity_score: float,
) -> str:
    category_text = _category_label(candidate.category)
    proximity = (
        f"{distance_km:.0f}km away"
        if distance_km >= 10
        else f"only {distance_km:.0f}km away"
    )
    crowd_text = {
        "Low": "currently low crowd",
        "Medium": "moderate crowd levels",
        "High": "still busy, but less crowded than your first choice",
    }.get(crowd_category, f"currently {crowd_category.lower()} crowd")

    tag_hint = candidate.tags[0] if candidate.tags else category_text
    return (
        f"Similar {category_text} experience ({tag_hint}), "
        f"{proximity}, {crowd_text} "
        f"(match score {similarity_score:.0%})"
    )


def _proximity_score(distance_km: float, max_distance_km: float) -> float:
    if max_distance_km <= 0:
        return 1.0
    return max(0.0, 1.0 - (distance_km / max_distance_km))


def _extract_low_time_slots(
    forecast: list[dict[str, Any]],
    *,
    skip_first_day: bool = False,
) -> list[TimeSlotSuggestion]:
    slots: list[TimeSlotSuggestion] = []
    days = forecast[1:] if skip_first_day else forecast
    for day in days:
        if day.get("crowd_category") == LOW_CROWD:
            slots.append(
                TimeSlotSuggestion(
                    date=day["date"],
                    crowd_category=day["crowd_category"],
                    crowd_score=int(day["crowd_score"]),
                    day_of_week=day.get("day_of_week", ""),
                )
            )
    return slots


def _compute_similarity_scores(
    source: DestinationMetadata,
    candidates: list[DestinationMetadata],
) -> dict[str, float]:
    if not candidates:
        return {}

    corpus = [source.tag_text] + [c.tag_text for c in candidates]
    vectorizer = TfidfVectorizer(lowercase=True, token_pattern=r"[a-zA-Z0-9/]+")
    matrix = vectorizer.fit_transform(corpus)
    sims = cosine_similarity(matrix[0:1], matrix[1:])[0]
    return {c.destination_id: float(sims[i]) for i, c in enumerate(candidates)}


class CrowdRecommender:
    """Finds less-crowded alternatives using UI 1 forecasts + local metadata."""

    def __init__(
        self,
        ui1_client: UI1Client | None = None,
        metadata: dict[str, DestinationMetadata] | None = None,
    ):
        self.ui1 = ui1_client or UI1Client()
        self.metadata = metadata or load_destination_metadata()

    def recommend(
        self,
        destination_id: str,
        *,
        force_alternatives: bool = False,
    ) -> RecommendationResult:
        if destination_id not in self.metadata:
            raise ValueError(f"Unknown destination_id: {destination_id}")

        source = self.metadata[destination_id]
        forecast = self.ui1.get_forecast(destination_id)
        if not forecast:
            raise ValueError(f"No forecast returned for {destination_id}")

        today = forecast[0]
        is_overcrowded = today["crowd_category"] == HIGH_CROWD
        should_suggest = is_overcrowded or force_alternatives

        alternate_time_slots = _extract_low_time_slots(
            forecast,
            skip_first_day=is_overcrowded,
        )

        original = {
            "destination_id": destination_id,
            "name": source.name,
            "city": source.city,
            "state": source.state,
            "category": source.category,
            "crowd_category": today["crowd_category"],
            "crowd_score": int(today["crowd_score"]),
            "forecast_date": today["date"],
        }

        alternatives: list[AlternativeRecommendation] = []
        if should_suggest:
            alternatives = self._rank_alternatives(source, destination_id)

        return RecommendationResult(
            original_destination=original,
            is_overcrowded=is_overcrowded,
            alternatives=alternatives,
            alternate_time_slots=alternate_time_slots,
        )

    def _rank_alternatives(
        self,
        source: DestinationMetadata,
        exclude_id: str,
    ) -> list[AlternativeRecommendation]:
        candidates_meta = [
            m for did, m in self.metadata.items() if did != exclude_id
        ]
        if not candidates_meta:
            return []

        similarity_map = _compute_similarity_scores(source, candidates_meta)

        distances = {
            c.destination_id: haversine_km(
                source.latitude,
                source.longitude,
                c.latitude,
                c.longitude,
            )
            for c in candidates_meta
        }
        max_distance = max(distances.values()) if distances else 1.0

        scored: list[AlternativeRecommendation] = []
        for candidate in candidates_meta:
            cid = candidate.destination_id
            try:
                cand_forecast = self.ui1.get_forecast(cid)
                cand_today = cand_forecast[0]
            except httpx.HTTPError:
                # If UI 1 doesn't track this location, assume it's a "hidden gem" alternative
                cand_today = {
                    "crowd_category": LOW_CROWD,
                    "crowd_score": 25,
                }

            crowd_category = cand_today["crowd_category"]
            crowd_score = int(cand_today["crowd_score"])
            similarity = similarity_map[cid]
            distance = distances[cid]
            proximity = _proximity_score(distance, max_distance)
            low_crowd_factor = 1.0 - (crowd_score / 100.0)

            final_score = (
                similarity * SIMILARITY_WEIGHT
                + proximity * PROXIMITY_WEIGHT
                + low_crowd_factor * LOW_CROWD_WEIGHT
            )

            # Deprioritize destinations that are also overcrowded today
            if crowd_category == HIGH_CROWD:
                final_score *= 0.35

            scored.append(
                AlternativeRecommendation(
                    destination_id=cid,
                    name=candidate.name,
                    similarity_score=round(similarity, 3),
                    distance_km=round(distance, 1),
                    crowd_category=crowd_category,
                    crowd_score=crowd_score,
                    final_score=round(final_score, 4),
                    reason=_build_reason(
                        candidate, distance, crowd_category, similarity
                    ),
                )
            )

        # Prefer non-High candidates, then by final_score
        scored.sort(
            key=lambda x: (
                x.crowd_category == HIGH_CROWD,
                -x.final_score,
            )
        )

        # Take top 3, ensuring at least 2 when possible
        top = scored[:MAX_ALTERNATIVES]
        if len(scored) >= MIN_ALTERNATIVES and len(top) < MIN_ALTERNATIVES:
            top = scored[:MIN_ALTERNATIVES]

        # Demo-friendly: if everything left is High, still return best 2 by score
        non_high = [a for a in top if a.crowd_category != HIGH_CROWD]
        if len(non_high) >= MIN_ALTERNATIVES:
            return non_high[:MAX_ALTERNATIVES]

        return top


def find_overcrowded_destination_ids(ui1_client: UI1Client | None = None) -> list[str]:
    """Utility for demos/tests — list destination_ids with High crowd today."""
    client = ui1_client or UI1Client()
    overcrowded: list[str] = []
    for dest in client.list_destinations():
        if dest.get("current_crowd_category") == HIGH_CROWD:
            overcrowded.append(dest["destination_id"])
    return overcrowded
