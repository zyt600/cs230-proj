cd progrmr-anon/evaluation/
bash throughput.sh -t 5 -d CSV -m gf -p p
bash wellformedness.sh -d CSV -p p
cd ../../fandango/
echo "Evaluating CSV Grammar in Fandango for throughput and well-formedness:"
python3 ./evaluation/csv/csv_evaluation.py
# echo "Evaluating XML Grammar in Fandango for throughput and well-formedness:"
# python3 evaluation/xml/xml_evaluation.py
# echo "Evaluating REST Grammar in Fandango for throughput and well-formedness:"
# python3 evaluation/rest/rest_evaluation.py