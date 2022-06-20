cd ./tests
for test in $(ls)
do
python3 $test
done
