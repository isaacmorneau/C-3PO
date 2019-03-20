#include <stdio.h>

#pragma c3po mangle(name)
void foobar(void) {
    puts("hello world");
}

int main(void) {
#pragma c3po encrypt
    foobar();
    return 0;
}
