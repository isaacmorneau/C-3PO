#!/usr/bin/bash
#unit tests
echo "==> unit tests"
./c3po.py test
#integration tests
echo "==> preparing for integration tests"
./c3po.py test/src test/gen/ c823d57855

echo "==> integration tests"
for f in test/gen/*.c; do
    echo "diffing $f and $f.valid"
    diff -qy "$f" "$f.valid"
done
echo "==> complete"

