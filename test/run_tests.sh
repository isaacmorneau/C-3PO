#!/usr/bin/bash
#unit tests
echo "==> unit tests"
../c3po.py test --quiet
#the following is used for the unit tests for post processing
#clang gen/encrypt.c ../src/c3po.c -I ../src -Os -o post_unittest

#integration tests
echo "==> preparing for integration tests"
mkdir -p gen
#run encrypt last so the c3po.json is correct
TESTS=(basic assert mangle shatter shuffle encrypt)
for test in ${TESTS[@]};
do
    printf "building original $test"
    gcc ../src/c3po.c "$test/$test.c" -I ../src/ -o "gen/${test}d"
    printf ", generating c3po $test"
    ../c3po.py build -s "$test" -o gen/ --seed c823d57855 --quiet
    echo ", building c3po $test"
    gcc ../src/c3po.c "gen/$test.c" -I ../src/ -o "gen/$test"
done
#finish the encryption pass
../c3po.py post -s "gen/encrypt" --json ./c3po.json --quiet

echo "==> integration tests"
for f in gen/*.c; do
    diff -qy "$f" "$f.valid" && echo "$f OK"
done
echo "==> complete"

