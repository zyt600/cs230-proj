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
while getopts "d:p:s" opt; do
    case $opt in
        d) TESTED_DOMAINS=$OPTARG ;; # Domains to test
        p) PROGRAMS=$OPTARG ;; # Programs to test
        s) SHOW_FAILURES=1 ;; # Show failures
        *) echo "Usage: $0 [-d domains] [-p programs] [-s show_failures]" >&2; exit 1 ;;
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

SHOW_FAILURES=${SHOW_FAILURES:-0} # Default don't show failures


### Define directories and files
EVAL_DIR="./evaluation_results"
OUTPUT="./evaluation_results/wellformedness.txt"
LOG="output.txt"
echo "-----" >> $OUTPUT
rm $LOG


### Run tests for each program
for program in "${PROGRAMS[@]}"; do
    echo -e "${MAGENTA}------------------------------------------------------------------${RESET}"
    echo -e "${MAGENTA}Getting wellformedness for ${YELLOW}$program${RESET}"
    echo -e "${MAGENTA}------------------------------------------------------------------${RESET}"
    
    for domain in "${TESTED_DOMAINS[@]}"; do
        echo -e "${BLUE}-------------------------------------${RESET}"
        echo -e "${BLUE}Getting wellformedness for domain: ${YELLOW}$domain${RESET}"
        echo -e "${BLUE}-------------------------------------${RESET}"

        in_dir="$EVAL_DIR/$program/$domain/unique"
        if [[ "$program" == "grammarinator" ]]; then
            out_dir="$EVAL_DIR/$program/$domain/$base_name/wellformed/"
            rm -r $out_dir
            mkdir -p $out_dir
        else

            out_dir="/tmp/"

        fi

        input_size=$(find $in_dir -type f | wc -l)
        if [[ $input_size -eq 0 ]]; then
            echo -e "${RED}No files found in $in_dir${RESET}"
            continue
        fi
        echo -e "${CYAN}Processing: ${YELLOW}$input_size files ${CYAN}from${YELLOW} $in_dir${RESET}"
        
        progress=0
        wellformed=0

        if [[ $SHOW_FAILURES == 1 ]]; then
            for file in "$in_dir"/*; do

                # Test if the file is wellformed
                # if [[ "$(cat $file)" == "{}" || $(timeout 10 isla check isla/$domain/grammar.py -c true -i "$(cat $file)") == *"satisfies"* ]];
                if python3 acceptance_checkers/main.py -d $domain -f $file >> $LOG 2>&1; 
                then

                    wellformed=$((wellformed + 1))
                    if [[ "$program" == "grammarinator" ]]; then
                        cp "$file" "$out_dir"
                    fi

                else

                    echo -e "${RED}File ${YELLOW}$file${RED} is not wellformed.${RESET}                             "
                    echo -e "${RED}    Command: ${YELLOW}python3 acceptance_checkers/main.py -d $domain -f $file${RESET}"
                
                fi

                progress=$((progress + 1))
                percent=$((progress * 100 / input_size))
                echo -ne "${CYAN}Progress: [${GREEN}$(printf '#%.0s' $(seq 1 $((percent / 2))))${RESET}$(printf '.%.0s' $(seq 1 $((50 - percent / 2))))${BLUE}] ${YELLOW}$progress${RESET} / ${YELLOW}$input_size${RESET} (${YELLOW}$percent%${RESET}) | Wellformedness: ${GREEN}$wellformed${RESET} / ${YELLOW}$progress${RESET} (${YELLOW}$((wellformed * 100 / progress))%${RESET})\r"

            done

            echo ""
            
            wellformedness=$((wellformed * 100 / input_size))
            echo -e "${GREEN}Wellformedness: ${YELLOW}$wellformed${RESET} / ${YELLOW}$input_size${RESET} (${YELLOW}$wellformedness%${RESET})"
            echo "$program,$domain: $wellformed / $input_size" >> $OUTPUT

        else

            python3 acceptance_checkers/parallel_main.py --directory $in_dir -d $domain -p $program -o $OUTPUT --od $out_dir 2> $LOG

        fi

        echo ""

    done

    echo -e "${MAGENTA}Wellformedness evaluation for $program completed.${RESET}"

done
