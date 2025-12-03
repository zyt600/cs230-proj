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
while getopts "t:d:p:m:" opt; do
    case $opt in
        t) TIMEOUT=$OPTARG ;; # Timeout value
        d) TESTED_DOMAINS=$OPTARG ;; # Domains to test
        p) PROGRAMS=$OPTARG ;; # Programs to test
        m) MODE=$OPTARG ;; # Generate and filter unique, just generate, or just filter
        *) echo "Usage: $0 [-t timeout] [-d domains] [-p programs] [-m mode]" >&2; exit 1 ;;
    esac
done

TIMEOUT=${TIMEOUT:-300} # Default timeout: 5 minutes/300 seconds
echo -e "Testing with timeout: $TIMEOUT seconds"

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

MODE=${MODE:-"gf"} # Default to both generate and filter
echo -e "Mode: $MODE"


### Define directories and files
# Input variable: where the ProGRMR repo lives (can be overridden via env var PROGRMR_REPO_DIR)
PROGRMR_REPO_DIR="${PROGRMR_REPO_DIR}"
# Input variable: where evaluation output should be directed (can be overridden via env var OUTPUT_BASE_DIR)
OUTPUT_BASE_DIR="${OUTPUT_BASE_DIR}"

EVAL_DIR="$OUTPUT_BASE_DIR"
PROGRMR_COMPILER="$PROGRMR_REPO_DIR/ProGRMR/main.py"
PROGRMR_DIR="$PROGRMR_REPO_DIR/evaluation/progrmr"
ISLA_DIR="$PROGRMR_REPO_DIR/isla"
GRAMMATINATOR_DIR="$PROGRMR_REPO_DIR/grammarinator"
OUTPUT="$OUTPUT_BASE_DIR/throughput.txt"
LOG="output.txt"
GRAMMARINATOR_OUTPUT="%d.txt"
mkdir -p $EVAL_DIR
echo "-----" >> $OUTPUT
echo "" > $LOG


### Set configs
# REMEMBER TO SET THE CONFIGS ACCORDING TO ISLA'S FROM THEIR EVAL SCRIPTS
declare -A ISLA_CONFIGS # ISLA_CONFIGS["DOMAIN"] = ("CSV OF WEIGHT_VECTOR" MAX_FREE_INST MAX_SMT_INST EVAL_K)
ISLA_CONFIGS["C"]="   -w 5,2,6,2,21     -f 10 -s 2 -k 3" # Configs from isla/evaluations/evaluate_scriptsize_c.py
ISLA_CONFIGS["CSV"]=" -w 1,0,1,0,0      -f 10 -s 5 -k 3" # Configs from isla/evaluations/evaluate_csv.py
ISLA_CONFIGS["REST"]="-w 7,1.5,2.5,2,18 -f 10 -s 2 -k 4" # Configs from isla/evaluations/evaluate_rest.py
ISLA_CONFIGS["MLIR"]="                                 " # None available
ISLA_CONFIGS["XML"]=" -w 10,0,6,0,13    -f 10 -s 2 -k 4" # Configs from isla/evaluations/evaluate_xml.py
ISLA_CONFIGS["simpleC"]="                              "
ISLA_CONFIGS["JSON"]="                                 "


### Compile the ProGRMR meta-grammar
java -jar /usr/local/lib/antlr-4.13.2-complete.jar -Dlanguage=Python3 $PROGRMR_REPO_DIR/ProGRMRParser.g4 $PROGRMR_REPO_DIR/ProGRMRLexer.g4


### Run tests for each program
for program in "${PROGRAMS[@]}"; do
    echo -e "${MAGENTA}------------------------------------------------------------------${RESET}"
    echo -e "${MAGENTA}Getting throughput for ${YELLOW}$program${RESET}"
    echo -e "${MAGENTA}------------------------------------------------------------------${RESET}"
    
    for domain in "${TESTED_DOMAINS[@]}"; do
        echo -e "${BLUE}-------------------------------------${RESET}"
        echo -e "${BLUE}Getting throughput for domain: ${YELLOW}$domain${RESET}"
        echo -e "${BLUE}-------------------------------------${RESET}"

        RESULT_DIR="$EVAL_DIR/$program/$domain/raw"

        ### GENERATION
        if [[ "$MODE" == *"g"* ]]; then
            rm -r $RESULT_DIR
            mkdir -p $RESULT_DIR

            echo -e "${CYAN}Generating files${RESET}"

            # Select a command based on the program
            # Grammarinator and ProGRMR need to be compiled first
            if [[ "$program" == "progrmr" ]]; then
                PROGRMR_OUTPUT="$PROGRMR_DIR/$domain/$domain.py"
                COMPILE_COMMAND="python3 $PROGRMR_COMPILER $PROGRMR_DIR/$domain/$domain.pg -o $PROGRMR_OUTPUT"
                echo -e "${CYAN}    Compiling: ${YELLOW} $COMPILE_COMMAND ${RESET}"
                eval $COMPILE_COMMAND >> $LOG 2>&1
                if [ $? -ne 0 ]; then
                    echo -e "${RED}    Error processing domain: ${YELLOW}$domain${RESET}"
                    echo -e "${RED}    Check ${YELLOW}$LOG${RED} for details.${RESET}"
                    continue
                fi
                COMMAND="python3 $PROGRMR_OUTPUT -t $TIMEOUT -n 0 -d $RESULT_DIR 2> $LOG"
            elif [[ "$program" == "isla" ]]; then
                constraint_files=$(ls $ISLA_DIR/$domain/*.isla | tr '\n' ' ')
                ARGS="-n -1 -t $TIMEOUT ${ISLA_CONFIGS[$domain]} -d $RESULT_DIR"
                COMMAND="isla solve $ISLA_DIR/$domain/grammar.py $constraint_files $ARGS"
            elif [[ "$program" == "grammarinator" ]]; then
                RESULT_FILE="$RESULT_DIR/$GRAMMARINATOR_OUTPUT"
                GRAMMAR_FILE="$GRAMMATINATOR_DIR/$domain/$domain.g4"
                echo -e "${CYAN}    Processing grammar file: ${YELLOW}$GRAMMAR_FILE${RESET}"
                grammarinator-process $GRAMMAR_FILE -o $GRAMMATINATOR_DIR/$domain/
                GENERATOR="${domain}Generator"
                ARGS="--sys-path $GRAMMATINATOR_DIR/$domain/ --no-mutate --stdout -n 999999999 -r start -j 1 -d 20 -o $RESULT_FILE"
                COMMAND="timeout $TIMEOUT grammarinator-generate $GENERATOR.$GENERATOR $ARGS -o $RESULT_FILE"
            else
                echo -e "${RED}    Unknown program: ${YELLOW}$program${RESET}"
                continue
            fi

            echo -e "${CYAN}    Running:${YELLOW} $COMMAND${RESET}"
            echo -e "${CYAN}    Current Time:${YELLOW}    $(TZ=America/Los_Angeles date)${RESET}"
            echo -e "${CYAN}    Completion Time:${YELLOW} $(TZ=America/Los_Angeles date -d "@$(( $(date +%s) + $TIMEOUT ))")${RESET}"

            # Generate throughput 
            eval $COMMAND >> $LOG 2>&1 &
            # With a nice progress bar
            pid=$!
            elapsed=0
            while kill -0 $pid 2>/dev/null; do
                progress=$((elapsed * 100 / (TIMEOUT)))
                if [[ $progress -gt 100 ]]; then
                    progress=100
                fi
                bar=$(printf "%-${progress}s" "#" | tr ' ' '#')
                dots=$(printf "%-$((100 - progress))s" "." | tr ' ' '.')
                echo -ne "${CYAN}    [${GREEN}${bar}${RESET}${dots}${CYAN}] ${YELLOW}${progress}% ${CYAN}(Elapsed: ${YELLOW}${elapsed}s${CYAN})\r"
                sleep 1
                ((elapsed++))
            done
            wait $pid
            echo -ne "\n"
            
            echo -e "${GREEN}Generated string count: ${YELLOW}$(find $RESULT_DIR -type f | wc -l)${GREEN} in $RESULT_DIR${RESET}"

            echo "$program,$domain:$(find $RESULT_DIR -type f | wc -l)/$TIMEOUT" >> $OUTPUT

        else
            echo -e "${CYAN}Skipping generation for ${YELLOW}$program${RESET}"
        fi


        ### FILTERING
        if [[ "$MODE" == *"f"* ]]; then

            echo -e "${CYAN}Creating unique files${RESET}"
            UNIQUE_DIR="$EVAL_DIR/$program/$domain/unique"
            rm -r $UNIQUE_DIR
            mkdir -p $UNIQUE_DIR

            input_size=$(find $RESULT_DIR -type f | wc -l)
            if [[ $input_size -eq 0 ]]; then
                echo -e "${RED}No files found in $RESULT_DIR${RESET}"
                continue
            fi
            echo -e "${CYAN}    Processing: ${YELLOW}$input_size ${CYAN}files${RESET}"
            
            # # Hash each files' content and use it as name in the output directory
            # # This will create a unique filename for each unique content, and duplicates will be ignored
            # processed=0
            # hash_set=()
            # for file in "$RESULT_DIR"/*; do
            #     if [[ -f "$file" ]]; then
            #         hash=$(sha256sum "$file" | awk '{print $1}')
            #         if [[ ! " ${hash_set[@]} " =~ " ${hash} " ]]; then
            #             hash_set+=("$hash")
            #             cp "$file" "$UNIQUE_DIR/$(basename "$file")"
            #         fi
            #     fi
            #     ((processed++))
            #     progress=$((processed * 100 / input_size))
            #     bar=$(printf "%-${progress}s" "#" | tr ' ' '#')
            #     dots=$(printf "%-$((100 - progress))s" "." | tr ' ' '.')
            #     echo -ne "    ${CYAN}[${GREEN}${bar}${RESET}${dots}${CYAN}] ${YELLOW}${progress}% ${CYAN}(${YELLOW}${processed}${CYAN}/${YELLOW}${input_size}${CYAN})\r"
            # done
            # echo -ne "\n"

            # output_size=$(find $UNIQUE_DIR -type f | wc -l)
            # echo -e "${CYAN}    Unique:  ${YELLOW}$output_size ${CYAN}files${RESET}"
            # echo -e "${CYAN}    Duplicates: ${YELLOW}$((input_size - output_size))${RESET}"

            # # Sometimes they can be too fast. Keep a random sample of 5000 files in the output directory
            # total_files=$(find "$UNIQUE_DIR" -type f | wc -l)
            # if [[ "$total_files" -gt 5000 ]]; then
            #     find "$UNIQUE_DIR" -type f | shuf | tail -n +5001 | xargs -I {} rm {}
            # fi
            # Faster with python
            COMPUTE_UNIQUES="$PROGRMR_REPO_DIR/evaluation/compute_uniques.py"
            python3 $COMPUTE_UNIQUES -i $RESULT_DIR -od $UNIQUE_DIR -o $OUTPUT -d $domain -p $program 

            unique_file_count=$(find "$UNIQUE_DIR" -type f | wc -l)
            echo -e "${GREEN}Generated unique and sampled count: ${YELLOW}$unique_file_count${GREEN} in $UNIQUE_DIR${RESET}"
  
        else
            echo -e "${CYAN}Skipping generation for ${YELLOW}$program${RESET}"
        fi

        echo ""

    done

    echo -e "${MAGENTA}Throughput for $program completed.${RESET}"

done
