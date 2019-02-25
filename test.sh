#!/usr/bin/bash
#unit tests
echo "==> unit tests"
./c3po.py test
#integration tests
echo "==> preparing for integration tests"
./c3po.py build -s test/src -o test/gen/ --seed c823d57855

echo "==> integration tests"
for f in test/gen/*.c; do
    diff -qy "$f" "$f.valid" && echo "$f OK"
done
echo "==> complete"

