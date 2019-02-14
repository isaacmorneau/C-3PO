#!/usr/bin/bash
#unit tests
./c3po.py test
#integration tests
./c3po.py test/src test/gen/ c823d57855

for f in test/gen/*.c; do
    diff -qy "$f" "$f.valid"
done
