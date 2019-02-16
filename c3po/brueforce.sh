#!/usr/bin/bash
OPCODES=$(grep -Er '<td>([0-9A-F]{2} )+'|grep -E 'em'|grep -Eo '([0-9A-F]{2})( [0-9A-F]{2})*'|sort|uniq)
echo "section .text" > t.asm
echo "global _start" >> t.asm
echo "_start:" >> t.asm
    #im going to make a rather big assumption, zeros are likely to be correlated to the smallest number of operands due to 3 factors
    #humans naturally count up
    #opcodes have gotten longer over time
    #the opcodes starting with F are far more complex and longer than lower ones
for O in $OPCODES;
do
    #write the bytes we know are real
    echo "$O" | sed -r "s/(^| )/\ndb 0x/g" >> t.asm
    #pad with nops
    for i in $(seq 1 $((15-$(echo "$O" | wc -w))));
    do
        echo "db 0x00" >> t.asm
    done
    #correct the offsets
    echo "db 0x90" >> t.asm
    echo "db 0x90" >> t.asm
    echo "db 0x90" >> t.asm
    echo "db 0x90" >> t.asm
    echo "db 0x90" >> t.asm
    echo "db 0x90" >> t.asm
    echo "db 0x90" >> t.asm
    echo "db 0x90" >> t.asm
    echo "db 0x90" >> t.asm
    echo "db 0x90" >> t.asm
    echo "db 0x90" >> t.asm
    echo "db 0x90" >> t.asm
    echo "db 0x90" >> t.asm
    echo "db 0x90" >> t.asm
    echo "db 0x90" >> t.asm
done
nasm -g -O0 -Wall -f elf t.asm -o t.o
ld -m elf_i386 t.o -o t
#this is currently the best way i can think of finding the smallest number of bytes per operand
objdump -dw t|grep -Eo '([0-9a-f]{2} )+\s*([a-z]+ )+'|sort|uniq
