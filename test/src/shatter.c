#include <stdio.h>

int main(void) {
#pragma c3po shatter(on)
    puts("testing");
    puts("shatter");
    puts("graphs");
#pragma c3po shatter(off)
#pragma c3po shatter(call, high, on)
    puts("1");
    puts("2");
    puts("3");
#pragma c3po shatter(off)
    return 0;
}