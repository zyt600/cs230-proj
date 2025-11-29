# erase existing fuzz input file if it exists
rm -f progrmr_fuzz_inputs.txt

# generate generator file
python3 /Users/jaredvelasquez/projects/progrmr-anon/ProGRMR/main.py progrmr_grammar.pg -o progrmr_generator.py
python3 progrmr_generator.py -n 1 > progrmr_fuzz_inputs.txt
echo "The following fuzz inputs have been saved to progrmr_fuzz_inputs.txt:"
cat progrmr_fuzz_inputs.txt
echo "Invoking program under test with fuzz inputs:"
python3 program_under_test.py -i progrmr_fuzz_inputs.txt