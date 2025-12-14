import csv
import io
import os
from pathlib import Path
import time
from io import StringIO

import dns.exception
import dns.zone
import dns.rdatatype
import dns.rdataclass

from fandango.evolution.algorithm import Fandango, LoggerLevel
from fandango.language.parse import parse


def is_syntactically_valid_dns(dns_string: str, origin: str = "example.com"):
    try:
        file_like = io.StringIO(dns_string)

        dns.zone.from_file(
            file_like,
            origin=origin,
            relativize=False,
            check_origin=False
        )
        return True
    except Exception:
        return False


def evaluate_dns(
    seconds=60,
) -> tuple[str, int, int, float, tuple[float, int, int], float, float]:
    here = Path(__file__).resolve().parent
    file_path = os.path.join(here, "dns.fan")
    with open(file_path, "r") as file:
        grammar, constraints = parse(file, use_stdlib=False)
        assert grammar is not None

    solutions = []

    time_in_an_hour = time.time() + seconds

    print("Generating DNS solutions...")
    fandango = Fandango(grammar, constraints, logger_level=LoggerLevel.ERROR)
    fan_gen = fandango.generate()
    for solution in fan_gen:
        solutions.append(solution)
        if time.time() >= time_in_an_hour:
            break

    print("Generating coverage...")
    coverage = grammar.compute_grammar_coverage(solutions, 4)

    valid = []
    for solution in solutions:
        if is_syntactically_valid_dns(str(solution)):
            valid.append(solution)

    set_mean_length = sum(len(str(x)) for x in valid) / len(valid)
    set_medium_length = sorted(len(str(x)) for x in valid)[len(valid) // 2]
    valid_percentage = len(valid) / len(solutions) * 100
    return (
        "DNS",
        len(solutions),
        len(valid),
        valid_percentage,
        coverage,
        set_mean_length,
        set_medium_length,
    )


if __name__ == "__main__":
    result = evaluate_dns(seconds=10)
    print(
        f"Type: {result[0]}, "
        f"Solutions: {result[1]}, "
        f"Valid: {result[2]}, "
        f"Valid Percentage: {result[3]:.2f}%, "
        f"Coverage: {result[4]}, "
        f"Mean Length: {result[5]:.2f}, "
        f"Medium Length: {result[6]:.2f}"
    )
