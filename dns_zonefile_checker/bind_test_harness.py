import os
import subprocess
import tempfile
import sys

BIND_IMAGE = "ubuntu/bind9:latest"
ORIGIN = "example.com"


def bind_test_harness(zone_text: str) -> bool:
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".zone") as f:
        f.write(zone_text)
        f.flush()
        zone_file_path = os.path.abspath(f.name)

    try:
        command = [
            "docker",
            "run",
            "--rm",
            "-v",
            f"{zone_file_path}:/zone.zone:ro",
            BIND_IMAGE,
            "named-checkzone",
            ORIGIN,
            "/zone.zone",
        ]

        os.makedirs("logs", exist_ok=True)

        # Redirect container stdout/stderr into host files
        with open("logs/out.txt", "wb") as out_f, open("logs/err.txt", "wb") as err_f:
            result = subprocess.run(command, stdout=out_f, stderr=err_f)

        print("Return code:", result.returncode)
        # Print contents of log files
        with open("logs/out.txt", "r") as out_f, open("logs/err.txt", "r") as err_f:
            print("STDOUT:", out_f.read())
            print("STDERR:", err_f.read())

        return result.returncode == 0
    finally:
        os.remove(zone_file_path)


def main():
    # Read entire zone file text from STDIN
    zone_text = sys.stdin.read()

    # BIND requires a trailing newline
    if not zone_text.endswith("\n"):
        zone_text += "\n"

    is_valid = bind_test_harness(zone_text)
    print("Zone is valid" if is_valid else "Zone is invalid")


if __name__ == "__main__":
    main()

