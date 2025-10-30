import argparse

def process_name_database_line(line: str):
    """
    Process a single line from the name database. A line in the name database looks like this:
    "first_name last_name,age"
    """
    name, age = line.split(",")
    first_name, last_name = name.split(" ")

    # Example cases that will be checked by Fandango and ProGRMR fuzzers:
    if 'E' in first_name:
        raise ValueError("First name contains invalid character 'E'")
    if 'X' in last_name:
        raise ValueError("Last name contains invalid character 'X'")
    if int(age) > 100:
        raise ValueError("Age exceeds maximum limit of 100")

    return {
        "first_name": first_name,
        "last_name": last_name,
        "age": int(age)
    }

def main():
    parser = argparse.ArgumentParser(description="Process a name database file.")
    parser.add_argument("-i", "--input_file", type=str, help="Path to the input name database file")
    args = parser.parse_args()

    with open(args.input_file, "r") as infile:
        for line in infile:
            line = line.strip()
            if line:
                processed = process_name_database_line(line)
                print(processed)

if __name__ == "__main__":
    main()