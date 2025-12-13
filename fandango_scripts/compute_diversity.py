import concurrent.futures
import time
from itertools import combinations
from pathlib import Path
from typing import Optional, Callable

from fandango.evolution.algorithm import Fandango, LoggerLevel
from fandango.language.parse import parse

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from textdistance import levenshtein
from tqdm import tqdm
import click

def generate_solutions(fan_path: Path, seconds: int) -> list[str]:
    with open(fan_path, "r") as f:
        grammar, constraints = parse(f, use_stdlib=False)
        assert grammar is not None

    fandango = Fandango(grammar, constraints, logger_level=LoggerLevel.ERROR)
    gen = fandango.generate()

    out: list[str] = []
    deadline = time.time() + seconds
    for sol in gen:
        out.append(str(sol))
        if time.time() >= deadline:
            break
    return out

def calculate_distance(s1: str, n1: str, s2: str, n2: str) -> dict:
    d = levenshtein.distance(s1, s2)
    return {
        "sample1": n1,
        "sample2": n2,
        "len1": len(s1),
        "len2": len(s2),
        "distance": d
    }

def calculate_distances_batch(batch: list[tuple[str, str, str, str]]) -> list[dict]:
    return [calculate_distance(a, an, b, bn) for (a, an, b, bn) in batch]

def plot_hist(df: pd.DataFrame, output_csv: Path) -> None:
    img_path = output_csv.with_suffix(".png")
    sns.displot(df, x="distance")
    mean = df["distance"].mean()
    plt.axvline(mean, color="red", linestyle="--")
    plt.text(mean + 1, plt.gca().get_ylim()[1] * 0.9, f"Avg: {mean:.2f}", color="red")
    plt.savefig(img_path)
    print(f"Saved histogram to {img_path}")
    print(f"Mean distance: {mean:.2f}")

@click.command()
@click.option("--grammar", "fan_path", required=True, type=click.Path(exists=True, path_type=Path),
              help="Path to a .fan grammar file.")
@click.option("--seconds", default=60, type=int, show_default=True,
              help="How long to generate samples for.")
@click.option("--output", "output_csv", required=True, type=click.Path(path_type=Path),
              help="Output CSV path (must end with .csv).")
@click.option("--workers", "num_workers", default=8, type=int, show_default=True)
@click.option("--executor", "executor_type", type=click.Choice(["process", "thread"]),
              default="thread", show_default=True)
@click.option("--batch-size", default=500, type=int, show_default=True)
@click.option("--max-samples", default=0, type=int, show_default=True,
              help="If > 0, truncate to at most this many generated samples (reduces O(n^2)).")
def main(
    fan_path: Path,
    seconds: int,
    output_csv: Path,
    num_workers: Optional[int],
    executor_type: str,
    batch_size: int,
    max_samples: int,
) -> None:
    assert output_csv.name.endswith(".csv"), "Output must be a .csv file."

    # 1) Generate
    samples = generate_solutions(fan_path, seconds)
    if max_samples and len(samples) > max_samples:
        samples = samples[:max_samples]

    n = len(samples)
    if n < 2:
        raise SystemExit(f"Need at least 2 samples, got {n}.")

    print(f"Generated {n} samples from {fan_path.name}")

    # 2) Build pair tasks (unique pairs only)
    # Name samples as s00001, s00002, ...
    named = [(samples[i], f"s{i:05d}") for i in range(n)]
    tasks = [(a, an, b, bn) for (a, an), (b, bn) in combinations(named, 2)]
    print(f"Total pairs: {len(tasks)}")

    executor_class = (
        concurrent.futures.ProcessPoolExecutor
        if executor_type == "process"
        else concurrent.futures.ThreadPoolExecutor
    )

    # 3) Parallel compute in batches
    results: list[dict] = []
    with executor_class(max_workers=num_workers) as ex:
        futures = []
        for i in range(0, len(tasks), batch_size):
            futures.append(ex.submit(calculate_distances_batch, tasks[i:i + batch_size]))

        with tqdm(total=len(futures), desc="Calculating Levenshtein distances") as pbar:
            for fut in concurrent.futures.as_completed(futures):
                results.extend(fut.result())
                pbar.update(1)

    # 4) Save + plot
    df = pd.DataFrame(results).sort_values("distance")
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_csv, index=False)
    print(f"Wrote {len(df)} rows to {output_csv}")
    plot_hist(df, output_csv)


if __name__ == "__main__":
    main()