import argparse
import sys
from C import compile_scriptsizec_clang
from CSV import csv_lint
from REST import render_rst
from MLIR import evaluate_mlir
from XML import validate_xml
from simpleC import compile_simplec_clang
from JSON import validate_json
from DNS import validate_dns
from TAR import validate_tar

# Take a string, return a bool for if it's accepted
acceptance_checkers = {
    "C": compile_scriptsizec_clang,
    "CSV": csv_lint,
    "REST": render_rst,
    "MLIR": evaluate_mlir,
    "XML": validate_xml,
    "simpleC": compile_simplec_clang,
    "JSON": validate_json,
    "DNS": validate_dns,
    "TAR": validate_tar
}

output = sys.stdout


def parse_arguments():
    parser = argparse.ArgumentParser(description="Acceptance Checker")
    parser.add_argument("-f", "--file", required=True, help="Path to the input file")
    parser.add_argument(
        "-d", "--domain", required=True, help="Domain of the input file"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()

    domain = args.domain
    acceptance_checker = acceptance_checkers[domain]

    file_path = args.file

    if domain == "MLIR":
        # MLIR requires the input to be a file path instead of a string
        passed = acceptance_checker(file_path, output)
        exit(0 if passed else 1)
    else:
        with open(file_path, "r") as file:
            input_data = file.read()
            passed = acceptance_checker(input_data, output)
            exit(0 if passed else 1)
