fandango fuzz -f namedb.fan -n 10

# Feed Inputs into a Single File
fandango fuzz -f namedb.fan -n 10 -o namedb.txt

# Feed Inputs into Individual Files
fandango fuzz -f namedb.fan -n 10 -d namedb

# Invoking Programs Directly
fandango fuzz -f namedb.fan -n 10 python program_under_test.py -i
fandango fuzz -f namedb_without_constrain.fan -n 10 python program_under_test.py -i
