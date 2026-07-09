import os
import sys
import subprocess
from pathlib import Path


def install_requirements():
    requirements_file = Path(__file__).resolve().parent / "requirements.txt"

    if not requirements_file.exists():
        print("\n❌ requirements.txt was not found.")
        print("Please create requirements.txt first.")
        sys.exit(1)

    print("\n❌ Some required Python packages are missing.")
    answer = input("Do you want to install required packages now? (yes/no): ")

    if answer.lower() in ["yes", "y"]:
        print("\nInstalling packages...\n")

        subprocess.check_call([
            sys.executable,
            "-m",
            "pip",
            "install",
            "-r",
            str(requirements_file)
        ])

        print("\n✅ Packages installed successfully.")
        print("Now run the command again:")
        print("    python manage.py runserver\n")
        sys.exit(0)

    else:
        print("\nPlease install packages manually:")
        print("    pip install -r requirements.txt\n")
        sys.exit(1)


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

    try:
        from django.core.management import execute_from_command_line
        execute_from_command_line(sys.argv)

    except ModuleNotFoundError:
        install_requirements()


if __name__ == "__main__":
    main()