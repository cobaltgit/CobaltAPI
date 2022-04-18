from uvicorn import run

import settings as s


def main() -> None:
    """
    Main function to run CobaltAPI app.
    """

    return run(app=s.APP, host=s.HOST, port=s.PORT, reload=s.DEBUG, access_log=s.ACCESS_LOG, workers=s.WORKERS)


if __name__ == "__main__":
    main()
