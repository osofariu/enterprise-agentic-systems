"""Shared Pydantic models for the maintenance personnel + docs surface.

These are the response shapes for two API endpoints:
  - POST /api/v1/maintenance/personnel-lookup
  - POST /api/v1/maintenance/docs

They live here so both the MCP tool layer (lesson 4) and the
training-recommender business logic can depend on a single typed contract
instead of passing dicts around.
"""

from typing import Optional

from pydantic import BaseModel


class PersonnelIssueBucket(BaseModel):
    """Per-(machine, reason_code) breakdown for a single person."""

    machine_id: str
    reason_code: str
    total_duration_hours: float
    average_duration_hours: float
    record_count: int


class MaintenancePersonnelBucket(BaseModel):
    """One person and the specific maintenance issues they were present for."""

    personnel_id: str
    personnel_name: Optional[str] = None
    total_duration_hours: float
    average_duration_hours: float
    record_count: int
    issues: list[PersonnelIssueBucket]


class MaintenanceDoc(BaseModel):
    """Documentation entry for a maintenance reason code."""

    reason_code: str
    reason_type: str  # 'description' | 'SOP' | 'training' | 'support'
    document: str


class TrainingRecommendation(BaseModel):
    """A single training recommendation with all context for human review."""

    personnel_id: str
    personnel_name: Optional[str] = None
    machine_id: str
    reason_code: str
    level: str  # RecommendationLevel value: 'recommend' | 'strongly_recommend'
    record_count: int
    total_duration_hours: float
    average_duration_hours: float
    reason_description: Optional[str] = None
    training_doc: Optional[str] = None
    approval_prompt: str = ''
