# erase existing fuzz input file if it exists
rm -f fandango_fuzz_inputs.txt

fandango fuzz -f namedb.fan -n 10 -o fandango_fuzz_inputs.txt
echo "The following fuzz inputs have been saved to fandango_fuzz_inputs.txt:"
cat fandango_fuzz_inputs.txt
echo "Invoking program under test with fuzz inputs:"
python3 program_under_test.py -i fandango_fuzz_inputs.txt