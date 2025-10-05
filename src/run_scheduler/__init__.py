import pathlib
import tomllib
import typing

import pydantic

from ._plan import PlanModel
from ._run import RunModel

T = typing.TypeVar("T", bound=pydantic.BaseModel)


def parse_config(model: typing.Type[T], file: pathlib.Path) -> T:
    with file.open("rb") as f:
        return model(**tomllib.load(f))


__all__ = ["PlanModel", "RunModel", "parse_config"]
