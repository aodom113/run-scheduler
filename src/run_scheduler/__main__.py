import shutil
from pathlib import Path

from run_scheduler import PlanModel, parse_config

if __name__ == "__main__":
    from argparse import ArgumentParser

    parse = ArgumentParser()
    parse.add_argument("config", type=Path)
    parse.add_argument("--output", "-o", type=Path, default=Path(__file__).parents[2] / "source")
    parse.add_argument("--force", "-f", action="store_true")
    args = parse.parse_args()

    model = parse_config(PlanModel, args.config.resolve())
    file: Path = args.output.resolve()
    file.mkdir(exist_ok=True)
    if args.force:
        for f in file.iterdir():
            if f.is_file():
                f.unlink()
            elif f.is_dir():
                shutil.rmtree(f)
    model.gen_rst(file)
