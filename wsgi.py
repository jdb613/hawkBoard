"""Application entry point."""
from application import create_app


def main(tst, tst1):
    app = create_app()
    app.run()


if __name__ == "__main__":
    main()
