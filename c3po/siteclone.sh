#!/usr/bin/bash
mkdir -p x86
OPTS=$(curl -s https://www.felixcloutier.com/x86/index.html | rg -o 'href="\..*?\.html'|cut -c9-|rev|cut -c6-|rev|sort|uniq)
for O in $OPTS;
do
    echo "fetching $O"
    CLN=${O//:/_}
    CLN=${CLN//-/_}
    curl -s https://www.felixcloutier.com/x86/$O > x86/$CLN
done
echo "done"

