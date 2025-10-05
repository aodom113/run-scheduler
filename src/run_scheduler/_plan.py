import datetime
from pathlib import Path
from typing import Any

import tomli_w
from pydantic import BaseModel, Field

from . import _run


def _header(header: str) -> str:
    return f"{header}\n{'=' * len(header)}\n"


def _subheader(subheader: str) -> str:
    return f"{subheader}\n{'-' * len(subheader)}\n"


def _section(section: str) -> str:
    return f"{section}\n{'^' * len(section)}\n"


_weekday = {
    0: "monday",
    1: "tuesday",
    2: "wednesday",
    3: "thursday",
    4: "friday",
    5: "saturday",
    6: "sunday",
}


class _DayModel(BaseModel):
    date_: datetime.datetime = Field(alias="date")
    run_: _run.RunModel = Field(default_factory=lambda: _run.RunModel(), alias="run")

    def rst(self) -> str:
        return (
            f"{_subheader(_weekday[self.date_.weekday()].capitalize())}"
            f"{_section('Run')}{self.run_.rst()}"
        )


class PlanModel(BaseModel):
    days_: list[_DayModel] = Field(alias="days")

    def model_post_init(self, context: Any) -> None:  # noqa: ANN401
        self.days_.sort(key=lambda d: d.date_)
        return super().model_post_init(context)

    def gen_rst(self, target: Path, project: str = "Training Plan", author: str = "None") -> None:
        if not target.exists():
            msg = f"{target} does not exist"
            raise ValueError(msg)
        if not target.is_dir():
            msg = f"{target} is not a directory"
            raise ValueError(msg)
        if any(target.iterdir()):
            msg = f"{target} is not empty"
            raise ValueError(msg)

        with Path.open(target / "conf.py", "wb") as file:
            data = {
                "project": project,
                "copyright": f"{datetime.datetime.now(tz=datetime.timezone.utc).date()}, {author}",
                "author": author,
                "extensions": ["sphinx_book_theme", "sphinx_copybutton"],
                "templates_path": ["_templates"],
                "exclude_patterns": [],
                "html_theme": "sphinx_book_theme",
                "html_static_path": ["_static"],
            }
            tomli_w.dump(data, file)

        Path.mkdir(target / "_static")
        Path.mkdir(target / "_templates")

        months: dict[Path, list[list[_DayModel]]] = {}
        for d in self.days_:
            month = target / d.date_.strftime("%Y-%m")
            if month not in months:
                months[month] = [[d]]
            else:
                if d.date_.weekday() == 0:
                    months[month].append([d])
                else:
                    months[month][-1].append(d)

        for m, w in months.items():
            m.mkdir()
            with Path.open(m / f"{m.name}.rst", "w") as f:
                f.write(
                    _header(
                        datetime.datetime.strptime(m.name, "%Y-%m")
                        .astimezone(datetime.timezone.utc)
                        .strftime("%B %Y")
                    )
                )
                f.write(".. toctree::\n\t:maxdepth: 1\n\t:glob:\n\n\t*\n")
            for i in range(len(w)):
                name = f"{w[i][0].date_.date()}-{w[i][-1].date_.date()}.rst"
                with Path.open(m / name, "w") as f:
                    f.write(_header(f"Week {i + 1}"))
                    for d in w[i]:
                        f.write(d.rst())

        with Path.open(target / "index.rst", "w") as f:
            f.write(".. toctree::\n\t:maxdepth: 2\n\t:caption: Contents\n\n")
            for m in target.glob("[0-9][0-9][0-9][0-9]-[0-9][0-9]"):
                if Path.exists(m / f"{m.name}.rst"):
                    f.write(f"\t{m.name}/{m.name}\n")
                # d in m.iterdir():
                #    f.write(f"\t{m.name}/{d.stem}\n")
