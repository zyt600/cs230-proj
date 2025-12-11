import argparse
import subprocess
import sys
import os

DOMAINS = ["REST", "XML", "CSV"]

def _generate_fandango_metrics(fandango_dir: str):
    pass

def _run_progrmr_script(
    script_name: str,
    progrmr_repo_dir: str,
    output_dir: str,
    extra_args: list[str],
) -> None:
    """
    Common helper to run a ProGRMR evaluation script (throughput.sh or wellformed.sh).

    - script_name: 'throughput.sh' or 'wellformed.sh'
    - progrmr_repo_dir: path to progrmr-anon repo (contains evaluation/, ProGRMR/, etc.)
    - output_dir: directory where evaluation_results should live
    - extra_args: extra CLI args for the script (e.g. ['-d', 'CSV', '-m', 'gf', '-p', 'p'])
    """
    # Normalize paths
    progrmr_repo_dir = os.path.abspath(progrmr_repo_dir)
    output_dir = os.path.abspath(output_dir)

    # Script is in evaluation/<script_name> inside the repo
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(cur_dir, "progrmr_scripts", script_name)
    if not os.path.isfile(script_path):
        raise FileNotFoundError(
            f"Could not find {script_name} at {script_path}. "
        )

    # Environment overrides (used by your modified scripts)
    env = os.environ.copy()
    env["PROGRMR_REPO_DIR"] = progrmr_repo_dir
    env["OUTPUT_BASE_DIR"] = output_dir

    cmd = ["bash", script_path] + extra_args

    print(f"\nRunning {script_name}:")
    print(f"  PROGRMR_REPO_DIR = {progrmr_repo_dir}")
    print(f"  OUTPUT_BASE_DIR  = {output_dir}")
    print(f"  Command: {' '.join(cmd)}\n")

    result = subprocess.run(
        cmd,
        cwd=progrmr_repo_dir,  # so relative paths inside the script work
        env=env,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(f"{script_name} failed with exit code {result.returncode}")
    
def _run_progrmr_throughput(
    progrmr_repo_dir: str,
    output_dir: str,
    domain: str,
    timeout: int = 100,
    mode: str = "gf",
    programs: str = "p",
) -> None:
    """
    Run throughput.sh for a single domain (e.g. 'CSV', 'XML', 'REST').

    - progrmr_repo_dir: progrmr-anon repo root
    - output_dir: where evaluation_results should go
    - domain: 'CSV', 'XML', 'REST', etc.
    - timeout: timeout in seconds (maps to -t)
    - mode: ProGRMR mode (e.g. 'gf' for generate+filter)
    - programs: program string (e.g. 'p' for ProGRMR only, 'progrmr,isla')
    """
    extra_args = [
        "-t", str(timeout),
        "-d", domain,
        "-m", mode,
        "-p", programs,
    ]
    _run_progrmr_script("throughput.sh", progrmr_repo_dir, output_dir, extra_args)

def _run_progrmr_wellformedness(
    progrmr_repo_dir: str,
    output_dir: str,
    domain: str,
    programs: str = "p",
    show_failures: bool = False,
) -> None:
    """
    Run wellformed.sh for a single domain (e.g. 'CSV', 'XML', 'REST').

    - progrmr_repo_dir: progrmr-anon repo root
    - output_dir: where evaluation_results should go (same OUTPUT_BASE_DIR)
    - domain: 'CSV', 'XML', 'REST', etc.
    - programs: program string (e.g. 'p' for ProGRMR only, 'progrmr,isla')
    - show_failures: if True, pass -s to show individual failing files
    """
    extra_args = [
        "-d", domain,
        "-p", programs,
    ]

    _run_progrmr_script("wellformedness.sh", progrmr_repo_dir, output_dir, extra_args)

def _copy_throughput_unique_files_to_wellformedness(
        output_dir: str,
        domain: str,
    ) -> None:
    """
    Copy unique files generated during throughput evaluation to the wellformedness
    evaluation directories
    """
    base_output_dir = os.path.abspath(output_dir)
    throughput_unique_dir = os.path.join(
        base_output_dir,
        "throughput",
        "progrmr",
        domain,
        "unique"
    )

    wellformedness_input_dir = os.path.join(
        base_output_dir,
        "wellformedness",
        "progrmr",
        domain,
        "unique"
    )

    os.makedirs(wellformedness_input_dir, exist_ok=True)
    for filename in os.listdir(throughput_unique_dir):
        src_file = os.path.join(throughput_unique_dir, filename)
        dst_file = os.path.join(wellformedness_input_dir, filename)
        subprocess.run(["cp", src_file, dst_file])

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

    parser.add_argument(
        '-t',
        '--timeout',
        type=int,
        default=100,
        help='Timeout in seconds for throughput evaluations.'
    )

    args = parser.parse_args(args)
    os.makedirs("progrmr_metrics", exist_ok=True)
    os.makedirs("fandango_metrics", exist_ok=True)

    print("\nGenerating Fandango metrics:\n")
    _generate_fandango_metrics(args.fandango_dir)

    for domain in DOMAINS:
        print(f"\nProcessing domain: {domain}")
        print("\nGenerating ProGRMR throughput metrics:\n")
        _run_progrmr_throughput(
            progrmr_repo_dir=args.progrmr_dir,
            output_dir=args.output_dir,
            domain=domain,
            timeout=args.timeout,
            mode="gf",
            programs="p",
        )

        # _copy_throughput_unique_files_to_wellformedness(
        #     output_dir=args.output_dir,
        #     domain=domain,
        # )

        print("\nGenerating ProGRMR wellformedness metrics:\n")
        _run_progrmr_wellformedness(
            progrmr_repo_dir=args.progrmr_dir,
            output_dir=args.output_dir,
            domain=domain,
            programs="p",
        )


if __name__ == "__main__":
    main(sys.argv[1:])