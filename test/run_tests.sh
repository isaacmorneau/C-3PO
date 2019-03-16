#!/usr/bin/bash
#unit tests
echo "==> unit tests"
../c3po.py test
#the following is used for the unit tests for post processing
#clang gen/encrypt.c ../src/c3po.c -I ../src -Os -o post_unittest

#integration tests
echo "==> preparing for integration tests"
mkdir -p gen
../c3po.py build -s basic/ -o gen/ --seed c823d57855
../c3po.py build -s assert/ -o gen/ --seed c823d57855
../c3po.py build -s mangle/ -o gen/ --seed c823d57855
../c3po.py build -s shatter/ -o gen/ --seed c823d57855
../c3po.py build -s shuffle/ -o gen/ --seed c823d57855
#run this last so the c3po.json is correct
../c3po.py build -s encrypt/ -o gen/ --seed c823d57855

echo "==> integration tests"
for f in gen/*.c; do
    diff -qy "$f" "$f.valid" && echo "$f OK"
done
echo "==> complete"

