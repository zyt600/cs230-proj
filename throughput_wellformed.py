import argparse
import subprocess
import sys
import os

DOMAINS = ["CSV", "REST", "XML"]

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
    output_throughput_dir = os.path.join(output_dir, "throughput")
    os.makedirs(output_throughput_dir, exist_ok=True)
    output_wellformed_dir = os.path.join(output_dir, "wellformed")
    os.makedirs(output_wellformed_dir, exist_ok=True)

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
    env["OUTPUT_BASE_DIR"] = output_throughput_dir

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
    print(f"  OUTPUT_BASE_DIR  = {output_throughput_dir}")
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
    
    wellformed_script = os.path.join(cur_dir, "progrmr_scripts", "wellformed.sh")
    if not os.path.isfile(wellformed_script):
        raise FileNotFoundError(
            f"Could not find wellformed.sh at {wellformed_script}. "
        )
    
    # Change environment for wellformed.sh
    env["OUTPUT_BASE_DIR"] = output_wellformed_dir
    
    # Now run wellformed.sh
    cmd = [
        "bash",
        wellformed_script,
        "-d", "CSV",
        "-p", "p"
    ]

    print(f"  PROGRMR_REPO_DIR = {progrmr_repo_dir}")
    print(f"  OUTPUT_BASE_DIR  = {output_wellformed_dir}")
    print(f"  Command: {' '.join(cmd)}\n")

    result = subprocess.run(
        cmd,
        cwd=progrmr_repo_dir,
        env=env,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"wellformed.sh failed with exit code {result.returncode}"
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