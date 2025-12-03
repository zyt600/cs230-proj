import argparse
import subprocess
import sys
import os

def _run_progrmr_throughput_command(command, cwd: str, log_dir: str):
    """
    Helper: run command in directory `cwd`, logging output.
    """
    os.makedirs(log_dir, exist_ok=True)
    print(f"  > Running in {cwd}:")
    print(f"    {' '.join(command)}\n")

    # ProGRMR's throughput.sh command's output logs can be modified via environment variables
    env = os.environ.copy()
    env["OUTPUT_BASE"] = log_dir

    result = subprocess.run(
        command,
        cwd=cwd,
        capture_output=True,
        text=True,
        env=env
    )

    std_path = os.path.join(log_dir, "output.log")

    with open(std_path, "w") as f:
        f.write("=== STDOUT ===\n")
        f.write(result.stdout)
        f.write("\n=== STDERR ===\n")
        f.write(result.stderr)

    if result.returncode != 0:
        raise RuntimeError(
            f"Command {' '.join(command)} failed with code {result.returncode}. "
            f"See log: {log_dir}"
        )

    print(f"Completed. Log: {log_dir}\n")

def _generate_fandango_metrics(fandango_dir: str):
    pass

def _generate_progrmr_metrics(progrmr_repo_dir: str, output_dir: str):
    # Normalize to absolute paths
    if not os.path.isabs(progrmr_repo_dir):
        progrmr_repo_dir = os.path.abspath(progrmr_repo_dir)
    if not os.path.isabs(output_dir):
        output_dir = os.path.abspath(output_dir)

    # Append progrmr to output_dir
    output_dir = os.path.join(output_dir)

    # throughput.sh lives in ./progrmr_scripts/throughput.sh
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    throughput_script = os.path.join(cur_dir, "progrmr_scripts", "throughput.sh")
    if not os.path.isfile(throughput_script):
        raise FileNotFoundError(
            f"Could not find throughput.sh at {throughput_script}. "
        )

    # Build environment with overrides
    env = os.environ.copy()
    env["PROGRMR_REPO_DIR"] = progrmr_repo_dir
    env["OUTPUT_BASE_DIR"] = output_dir

    # Same flags you were using manually: -t 5 -d CSV -m gf -p p
    cmd = [
        "bash",
        throughput_script,
        "-t", "5",
        "-d", "CSV",
        "-m", "gf",
        "-p", "p",
    ]

    print(f"  PROGRMR_REPO_DIR = {progrmr_repo_dir}")
    print(f"  OUTPUT_BASE_DIR  = {output_dir}")
    print(f"  Command: {' '.join(cmd)}\n")

    # Run with cwd = progrmr_dir so relative paths in the script match
    result = subprocess.run(
        cmd,
        cwd=progrmr_repo_dir,
        env=env,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"throughput.sh failed with exit code {result.returncode}"
        )

def main(args):
    parser = argparse.ArgumentParser("Perform Fandango and ProGRMR fuzzer evaluations to generate metrics.")

    parser.add_argument(
        '-f',
        '--fandango_dir',
        type=str,
        required=True,
        help='Directory containing Fandango repository.'
    )

    parser.add_argument(
        '-p',
        '--progrmr_dir',
        type=str,
        required=True,
        help='Directory containing ProGRMR repository.'
    )

    parser.add_argument(
        '-o',
        '--output_dir',
        type=str,
        default="metrics_output",
        help='Directory to output metrics.'
    )

    args = parser.parse_args(args)
    os.makedirs("progrmr_metrics", exist_ok=True)
    os.makedirs("fandango_metrics", exist_ok=True)

    print("\nGenerating Fandango metrics:\n")
    _generate_fandango_metrics(args.fandango_dir)
    print("\nGenerating ProGRMR metrics:\n")
    _generate_progrmr_metrics(args.progrmr_dir, args.output_dir)


if __name__ == "__main__":
    main(sys.argv[1:])