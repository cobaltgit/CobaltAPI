from json import load
from os import cpu_count

from uvicorn import run


def main():
    with open("config.json", "r") as cfg:
        config = load(cfg)
    run(**config, workers=cpu_count() * 2 + 1)


if __name__ == "__main__":
    main()
