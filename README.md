# CS230: An Evaluation of Fandango and ProGRMR Fuzzers
### Authors
Rajdeep Mondal, Adam Thieme, Jared Velasquez, Brian Yang, Yutong Zhou

### Overview
This project evaluates and compares Fandango and ProGRMR, two grammar-based fuzzers, on structured input domains (CSV, REST, XML, DNS, C, and JSON). The evaluation measures throughput, wellformedness, diversity, and coverage of the derivation space, which highlights the construction and tradeoffs between ProGRMR's high-throughput input generation and Fandango's coverage-based evolutionary input generation.

This repository contains custom grammars for both fuzzers, acceptance checkers, metric and computation scripts.

### Project Structure
`custom_grammars/`: Custom grammars and acceptance checkers / oracles for Fandango and ProGRMR.

`dns_zonefile_checker/`: Implementation of a DNS zone file test harness based on the [Bind](https://github.com/isc-projects/bind9) DNS name server implementation.

`fandango_scripts/`: Script to compute diversity metrics for Fandango outputs.
`progrmr_scripts/`: Scripts to compute throughput, wellformedness, and diversity metrics for ProGRMR outputs.

`metrics.py`: Metrics script to benchmark and evaluate ProGRMR and Fandango.

### Running the Experiments
First, install the dependencies via `pip3 install -r requirements.txt`. Also ensure that the [Fandango repository](https://github.com/fandango-fuzzer/fandango) and the [ProGRMR repository](https://github.com/qwerty373/progrmr-anon) are installed locally.

Metrics can be generated via the `metrics.py` script:
```sh
python3 metrics.py -f <FANDANGO_REPO> -p <PROGRMR_REPO> -t <TIMEOUT> -d <DOMAIN>
```

Currently supported domains: CSV, REST, XML, DNS, C, JSON