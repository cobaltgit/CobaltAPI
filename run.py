from json import load
from os import cpu_count

from uvicorn import run

from app import info


def main():
    if not all(map(info.get, ("name", "description", "version"))):
        raise RuntimeError("One of ('name', 'description', 'version') is not set in pyproject.toml")

    with open("config.json", "r") as cfg:
        config = load(cfg)
    run(**config, workers=cpu_count() * 2 + 1)


if __name__ == "__main__":
    main()
