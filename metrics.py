import argparse
import subprocess
import sys
import os
import shutil

# NOTE: to add a new domain, you will have to add its grammar to each repo's respective evaluation domain directories:

# Adding DNS to ProGRMR:
# Create the folder progrmr-anon/evaluation/progrmr/DNS, and add the grammar file DNS.pg there

FANDANGO_CUSTOM_DOMAINS = ["c"]

def _add_custom_domains_to_fandango(fandango_repo_dir: str) -> None:
    fandango_repo_dir = os.path.abspath(fandango_repo_dir)
    fandango_evaluation_dir = os.path.join(fandango_repo_dir, "evaluation")

    cur_dir = os.path.dirname(os.path.abspath(__file__))
    custom_grammars_path = os.path.join(cur_dir, "custom_grammars", "fandango")

    for domain in FANDANGO_CUSTOM_DOMAINS:
        # Copy custom grammars and checkers to Fandango
        domain_path = os.path.join(custom_grammars_path, domain)
        fandango_evaluation_domain_dir = os.path.join(fandango_evaluation_dir, domain)
        os.makedirs(fandango_evaluation_domain_dir, exist_ok=True)
        shutil.copytree(domain_path, fandango_evaluation_domain_dir, dirs_exist_ok=True)

    # ProGRMR bug: when evaluating, XML's evaluator tries to reference xml.etree but fails since the enclosing folder
    # is also called xml. This code resolves this.
    xml_original_path = os.path.join(fandango_evaluation_dir, "xml")
    if os.path.exists(xml_original_path):
        shutil.rmtree(xml_original_path)
    xml_fixed_path = os.path.join(custom_grammars_path, "xml")
    xml_fixed_fandango_path = os.path.join(fandango_evaluation_dir, "xml_test")
    if not os.path.exists(xml_fixed_fandango_path):
        shutil.copytree(xml_fixed_path, xml_fixed_fandango_path)

    # Do same with CSV, REST, and TAR
    csv_original_path = os.path.join(fandango_evaluation_dir, "csv")
    if os.path.exists(csv_original_path):
        shutil.rmtree(csv_original_path)
    csv_fixed_path = os.path.join(custom_grammars_path, "csv")
    csv_fixed_fandango_path = os.path.join(fandango_evaluation_dir, "csv_test")
    if not os.path.exists(csv_fixed_fandango_path):
        shutil.copytree(csv_fixed_path, csv_fixed_fandango_path)

    rest_original_path = os.path.join(fandango_evaluation_dir, "rest")
    if os.path.exists(rest_original_path):
        shutil.remtree(rest_original_path)
    rest_fixed_path = os.path.join(custom_grammars_path, "rest")
    rest_fixed_fandango_path = os.path.join(fandango_evaluation_dir, "rest_test")
    if not os.path.exists(rest_fixed_fandango_path):
        shutil.copytree(rest_fixed_path, rest_fixed_fandango_path)

    tar_original_path = os.path.join(fandango_evaluation_dir, "tar")
    if os.path.exists(tar_original_path):
        shutil.rmtree(tar_original_path)
    tar_fixed_path = os.path.join(custom_grammars_path, "tar")
    tar_fixed_fandango_path = os.path.join(fandango_evaluation_dir, "tar_test")
    if not os.path.exists(tar_fixed_fandango_path):
        shutil.copytree(tar_fixed_path, tar_fixed_fandango_path)

    # Do similar with DNS and JSON

    # DNS
    dns_fixed_path = os.path.join(custom_grammars_path, "dns")
    dns_fixed_fandango_path = os.path.join(fandango_evaluation_dir, "dns_test")
    if not os.path.exists(dns_fixed_fandango_path):
        shutil.copytree(dns_fixed_path, dns_fixed_fandango_path)

    # JSON
    json_fixed_path = os.path.join(custom_grammars_path, "json")
    json_fixed_fandango_path = os.path.join(fandango_evaluation_dir, "json_test")
    if not os.path.exists(json_fixed_fandango_path):
        shutil.copytree(json_fixed_path, json_fixed_fandango_path)
    
    # Copy acceptance checker runner
    main_path = os.path.join(custom_grammars_path, "run_evaluation.py")
    shutil.copy2(main_path, fandango_evaluation_dir)
    
def _run_fandango_evaluation(
        fandango_dir: str,
        output_dir: str,
        timeout: int = 100
):
    fandango_dir = os.path.abspath(fandango_dir)
    output_dir = os.path.abspath(output_dir)
    stdout_path = os.path.join(output_dir, "fandango_evaluation.txt")
    stderr_path = os.path.join(output_dir, "fandango_evaluation_err.txt")

    with open(stdout_path, "w") as out, open(stderr_path, "w") as err:
        run_evaluation_path = os.path.join(fandango_dir, "evaluation", "run_evaluation.py")
        cmd = ["python3", run_evaluation_path, str(timeout)]
        cwd = fandango_dir
        print(cmd)
        subprocess.run(
            cmd,
            cwd=cwd,
            stdout=out,
            stderr=err,
            text=True,
            check=True
        )

def _run_fandango_diversity(
        fandango_dir: str,
        output_dir: str,
        domain: str,
        timeout: int = 100,
        num_workers: int = 1,
        batch_size: int = 500,
        max_samples: int = 500,
    ):
    fandango_repo_dir = os.path.abspath(fandango_dir)
    output_dir = os.path.join(os.path.abspath(output_dir), domain)
    output_csv = os.path.join(output_dir, "diversity.csv")

    cur_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(cur_dir, "fandango_scripts", "compute_diversity.py")
    if not os.path.isfile(script_path):
        raise FileNotFoundError(
            f"Could not find compute_diversity.py at {script_path}"
        )
    
    domain_lower = domain.lower()
    custom_grammar_dir = os.path.join(cur_dir, "custom_grammars", "fandango", domain_lower)
    cmd_args = [
        "--grammar", os.path.join(custom_grammar_dir, f"{domain_lower}.fan"),
        "--seconds", str(timeout),
        "--output", output_csv,
        "--workers", str(num_workers),
        "--batch-size", str(batch_size),
        "--max-samples", str(max_samples)
    ]
    cmd = ["python3", script_path] + cmd_args

    print(f"\nRunning compute_diversity.py:")
    print(f"  PROGRMR_REPO_DIR = {fandango_repo_dir}")
    print(f"  OUTPUT_BASE_DIR  = {output_dir}")
    print(f"  Command: {' '.join(cmd)}\n")

    result = subprocess.run(
        cmd,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(f"compute_diversity.py failed with exit code {result.returncode}")

def _run_progrmr_script(
    script_name: str,
    progrmr_repo_dir: str,
    output_dir: str,
    extra_args: list[str],
    extra_env: dict[str, str] = {},
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
    for k, v in extra_env.items():
        env[k] = v

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
    
PROGRMR_CUSTOM_DOMAINS = ["DNS", "TAR"]

def _add_custom_domains_to_progrmr(progrmr_repo_dir: str) -> None:
    progrmr_repo_dir = os.path.abspath(progrmr_repo_dir)
    progrmr_evaluation_dir = os.path.join(progrmr_repo_dir, "evaluation")
    progrmr_evaluation_acceptance_dir = os.path.join(progrmr_evaluation_dir, "acceptance_checkers")
    progrmr_evaluation_grammars_dir = os.path.join(progrmr_evaluation_dir, "progrmr")

    cur_dir = os.path.dirname(os.path.abspath(__file__))
    custom_grammars_path = os.path.join(cur_dir, "custom_grammars", "progrmr")

    for domain in PROGRMR_CUSTOM_DOMAINS:
        # Copy custom acceptance checker to ProGRMR's acceptance checker dir
        domain_checker_path = os.path.join(custom_grammars_path, domain, f"{domain}.py")
        shutil.copy2(domain_checker_path, progrmr_evaluation_acceptance_dir)

        # Copy custom grammar to ProGRMR's grammar dir
        domain_grammar_path = os.path.join(custom_grammars_path, domain, f"{domain}.pg")
        os.makedirs(os.path.join(progrmr_evaluation_grammars_dir, domain), exist_ok=True)
        shutil.copy2(domain_grammar_path, os.path.join(progrmr_evaluation_grammars_dir, domain))

    # Copy acceptance checker runner
    main_path = os.path.join(custom_grammars_path, "main.py")
    shutil.copy2(main_path, progrmr_evaluation_acceptance_dir)

    
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

    if show_failures:
        extra_args.append("-s")

    _run_progrmr_script("wellformedness.sh", progrmr_repo_dir, output_dir, extra_args)

def _run_progrmr_diversity(
    progrmr_repo_dir: str,
    output_dir: str,
    domain: str,
) -> None:
    """
    Run diversity.sh for a single domain (e.g. 'CSV', 'XML', 'REST').

    - progrmr_repo_dir: progrmr-anon repo root
    - output_dir: where evaluation_results should go (same OUTPUT_BASE_DIR)
    - domain: 'CSV', 'XML', 'REST', etc.
    """
    extra_args = [
        "-d", domain,
        "-p", "progrmr"
    ]

    _run_progrmr_script("diversity.sh", progrmr_repo_dir, output_dir, extra_args)

def main(args):
    parser = argparse.ArgumentParser("Perform Fandango and ProGRMR fuzzer evaluations to generate metrics.")

    parser.add_argument(
        '-f',
        '--fandango_dir',
        type=str,
        help='Directory containing Fandango repository.'
    )

    parser.add_argument(
        '-r',
        '--run_fandango_eval',
        action='store_true',
        help='Run full Fandango evaluation over all grammars.'
    )

    parser.add_argument(
        '-p',
        '--progrmr_dir',
        type=str,
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

    parser.add_argument(
        '-d',
        '--domain',
        type=str,
        choices=["CSV", "XML", "REST", "DNS"],
        required=True,
        help='Specific domain to evaluate.'
    )

    args = parser.parse_args(args)

    if not args.fandango_dir and not args.progrmr_dir:
        raise ValueError("Either Fandango or ProGRMR repo directories must be provided.")

    domain = args.domain

    # append progrmr_metrics and fandango_metrics directories to output_dir
    progrmr_output_dir = os.path.join(args.output_dir, "progrmr_metrics")
    fandango_output_dir = os.path.join(args.output_dir, "fandango_metrics")
    os.makedirs(progrmr_output_dir, exist_ok=True)
    os.makedirs(fandango_output_dir, exist_ok=True)

    print(f"Processing domain: {domain}")

    if args.fandango_dir:
        print("\nCopying custom grammars to Fandango repo\n")
        _add_custom_domains_to_fandango(args.fandango_dir)

        if args.run_fandango_eval:
            _run_fandango_evaluation(args.fandango_dir, fandango_output_dir, args.timeout)

        print("\nGenerating Fandango diversity:\n")
        _run_fandango_diversity(args.fandango_dir, fandango_output_dir, domain, args.timeout)

    
    if args.progrmr_dir:
        print("\nCopying custom grammars to ProGRMR repo")
        _add_custom_domains_to_progrmr(args.progrmr_dir)
        print("\nGenerating ProGRMR throughput metrics:\n")
        # _run_progrmr_throughput(
        #     progrmr_repo_dir=args.progrmr_dir,
        #     output_dir=progrmr_output_dir,
        #     domain=domain,
        #     timeout=args.timeout,
        #     mode="gf",
        #     programs="p",
        # )

        # print("\nGenerating ProGRMR wellformedness metrics:\n")
        # # _run_progrmr_wellformedness(
        # #     progrmr_repo_dir=args.progrmr_dir,
        # #     output_dir=progrmr_output_dir,
        # #     domain=domain,
        # #     programs="p",
        # #     show_failures=True,
        # # )

        # print("\nGenerating ProGRMR diversity metrics:\n")
        # _run_progrmr_diversity(
        #     progrmr_repo_dir=args.progrmr_dir,
        #     output_dir=progrmr_output_dir,
        #     domain=domain,
        # )


if __name__ == "__main__":
    main(sys.argv[1:])