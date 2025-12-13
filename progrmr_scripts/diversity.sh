#!/bin/bash

### Define color codes
RED='\033[0;31m' # Error text
YELLOW='\033[0;33m' # Important text
GREEN='\033[0;32m' # Success text
BLUE='\033[0;34m' # Domain headers
CYAN='\033[0;36m' # Print text
MAGENTA='\033[0;35m' # Tool Text
RESET='\033[0m'


### Parse arguments
# Set defaults if not provided
while getopts "d:p:" opt; do
    case $opt in
        d) TESTED_DOMAINS=$OPTARG ;; # Domains to test
        p) PROGRAMS=$OPTARG ;; # Programs to test
        *) echo "Usage: $0 [-d domains] [-p programs]" >&2; exit 1 ;;
    esac
done

TESTED_DOMAINS=${TESTED_DOMAINS:-"C,CSV,REST,MLIR,XML"} # CSV of domains to test, default is all domains
echo -e "Tested domains: $TESTED_DOMAINS"
TESTED_DOMAINS=(${TESTED_DOMAINS//,/ }) # Turn CSV of domains into array

PROGRAMS=${PROGRAMS:-"progrmr,isla,grammarinator"} # CSV of programs to test, default is all programs
echo -e "Programs to test: $PROGRAMS"
PROGRAMS=(${PROGRAMS//,/ }) # Turn CSV of programs into array
for i in "${!PROGRAMS[@]}"; do # If any input is just the first letter, replace with full name
    case "${PROGRAMS[$i]}" in
        p) PROGRAMS[$i]="progrmr" ;;
        i) PROGRAMS[$i]="isla" ;;
        g) PROGRAMS[$i]="grammarinator" ;;
    esac
done


### Define directories and files
EVAL_DIR="${OUTPUT_BASE_DIR}"
PROGRMR_REPO_DIR="${PROGRMR_REPO_DIR}"


### Run tests for each program
for program in "${PROGRAMS[@]}"; do
    echo -e "${MAGENTA}------------------------------------------------------------------${RESET}"
    echo -e "${MAGENTA}Getting diversity for ${YELLOW}$program${RESET}"
    echo -e "${MAGENTA}------------------------------------------------------------------${RESET}"
    
    for domain in "${TESTED_DOMAINS[@]}"; do
        echo -e "${BLUE}-------------------------------------${RESET}"
        echo -e "${BLUE}Getting diversity for domain: ${YELLOW}$domain${RESET}"
        echo -e "${BLUE}-------------------------------------${RESET}"

        in_dir="$EVAL_DIR/$program/$domain/unique"
        if [[ "$program" == "grammarinator" ]]; then
            in_dir="$EVAL_DIR/$program/$domain/wellformed/"
        fi
        out_dir="$EVAL_DIR/$program/$domain/diversity/"
        rm -r $out_dir
        mkdir -p $out_dir

        out_file="$out_dir/diversity.csv"
        input_size=$(find $in_dir -type f | wc -l)
        if [[ $input_size -eq 0 ]]; then
            echo -e "${RED}No files found in $in_dir. Skipping domain: $domain.${RESET}"
            continue
        fi
        echo -e "${CYAN}Processing: ${YELLOW}$input_size files${RESET}"

        COMPUTE_DIVERSITY="$PROGRMR_REPO_DIR/evaluation/compute_diversity.py"
        python3 $COMPUTE_DIVERSITY --input $in_dir --output $out_file --workers 12 

        echo -e "${GREEN}Diversity evaluation for $domain completed.${RESET}"
        echo ""

    done

    echo -e "${MAGENTA}Diversity evaluation for $program completed.${RESET}"

done
