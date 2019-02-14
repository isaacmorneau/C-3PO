#include <stdio.h>

#pragma c3po cxor(on, 32)
#define hw "hello world"
#pragma c3po cxor(off)

#pragma c3po cxor(on)
#define em "this is an encrypted message"
#pragma c3po cxor(off)

int main(void) {
    return 0;
}
