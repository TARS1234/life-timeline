import re
from datetime import date
from typing import Optional
from pydantic import field_validator
from sqlmodel import SQLModel, Field


class MilestoneCreate(SQLModel):
    timeline_id: int
    parent_id: Optional[int] = None
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    target_date: Optional[date] = None
    end_date: Optional[date] = None
    target_year: int
    horizon_type: str = Field(default="year", max_length=20)
    category: str = Field(default="general", max_length=50)
    status: str = Field(default="planned", max_length=50)
    priority: str = Field(default="medium", max_length=20)
    position_order: int = 0
    color: Optional[str] = Field(default=None, max_length=7)
    notes: Optional[str] = Field(default=None, max_length=5000)

    @field_validator("color")
    @classmethod
    def validate_color(cls, v):
        if v is not None and not re.fullmatch(r"#[0-9a-fA-F]{6}", v):
            raise ValueError("color must be a hex value like #rrggbb")
        return v


class MilestoneUpdate(SQLModel):
    parent_id: Optional[int] = None
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    target_date: Optional[date] = None
    end_date: Optional[date] = None
    target_year: Optional[int] = None
    horizon_type: Optional[str] = Field(default=None, max_length=20)
    category: Optional[str] = Field(default=None, max_length=50)
    status: Optional[str] = Field(default=None, max_length=50)
    priority: Optional[str] = Field(default=None, max_length=20)
    position_order: Optional[int] = None
    color: Optional[str] = Field(default=None, max_length=7)
    notes: Optional[str] = Field(default=None, max_length=5000)

    @field_validator("color")
    @classmethod
    def validate_color(cls, v):
        if v is not None and not re.fullmatch(r"#[0-9a-fA-F]{6}", v):
            raise ValueError("color must be a hex value like #rrggbb")
        return v


class NoteCreate(SQLModel):
    timeline_id: int
    content: str = Field(min_length=1, max_length=5000)


class TimelineUpdate(SQLModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=500)
    start_year: Optional[int] = None
    end_year: Optional[int] = None
