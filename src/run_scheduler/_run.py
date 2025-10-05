import datetime
from typing import Literal

from pydantic import BaseModel, Field


class _RunModel(BaseModel):
    unit_: Literal["mi, km", "m"] = Field(default="mi", alias="unit")  # pyright: ignore[reportAssignmentType]
    distance_: float = Field(default=0.0, ge=0.0, alias="distance")
    time_: datetime.timedelta = Field(
        default_factory=lambda: datetime.timedelta(), ge=datetime.timedelta(), alias="time"
    )


class _SetModel(_RunModel):
    unit_: Literal["mi, km", "m"] = Field(default="m", alias="unit")
    reps_: int = Field(default=1, ge=1, alias="reps")


class _WorkoutModel(BaseModel):
    warm_up_: _RunModel = Field(default_factory=lambda: _RunModel(), alias="warm_up")
    workout_: list[_SetModel] = Field(default_factory=list, alias="workout")
    class_: Literal["T", "I", "S", ""] = Field(default="", alias="class")
    cool_down_: _RunModel = Field(default_factory=lambda: _RunModel(), alias="cool_down")


class RunModel(_RunModel, _WorkoutModel):
    def rst(self) -> str:
        return ""
