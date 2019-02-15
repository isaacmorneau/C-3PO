#include <stdio.h>
int main(void) {
#pragma c3po shuffle(on)
    puts("1");
#pragma c3po case
    puts("2");
#pragma c3po case
    puts("3");
#pragma c3po case
    puts("4");
#pragma c3po shuffle(off)
}
