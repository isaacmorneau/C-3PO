#include <stdio.h>

int main(void) {
#pragma c3po timer(main, on)
    puts("hello world");
    fputs("hello world", stderr);
#pragma c3po timer(main, 60000)
    puts("hello world");
    fputs("hello world", stderr);
#pragma c3po timer(main, 1000, 20000)
    return 0;
}
