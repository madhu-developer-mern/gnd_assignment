import os
import subprocess
import sys
import venv
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PROJECT = ROOT / "Django-Backend-Assessment" / "project"
VIRTUAL_ENV = ROOT / ".venv"
VIRTUAL_PYTHON = VIRTUAL_ENV / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def run_python(*arguments):
    subprocess.run([str(VIRTUAL_PYTHON), *arguments], cwd=PROJECT, check=True)


def setup():
    if sys.version_info < (3, 11):
        sys.exit("Setup requires Python 3.11 or newer.")
    if not VIRTUAL_PYTHON.is_file():
        venv.create(VIRTUAL_ENV, with_pip=True)

    run_python("-m", "pip", "--disable-pip-version-check", "install", "--only-binary=:all:",
               "-r", "requirements.txt")
    (PROJECT / "data").mkdir(exist_ok=True)
    run_python("manage.py", "migrate", "--noinput")
    run_python("manage.py", "seed_items")
    print("Setup complete. Run python manage.py runserver to start the API.")


def main(arguments):
    if arguments == ["setup"]:
        setup()
    elif not arguments:
        print("Usage: python manage.py setup | <Django command>")
    elif not VIRTUAL_PYTHON.is_file():
        sys.exit("Run python manage.py setup first.")
    else:
        run_python("manage.py", *arguments)


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except subprocess.CalledProcessError as error:
        sys.exit(error.returncode)
    except KeyboardInterrupt:
        sys.exit(130)
