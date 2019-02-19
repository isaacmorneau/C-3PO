#include <stdint.h>
#include <stdio.h>
#include <stdarg.h>
#include <stdbool.h>

#include "c3po.h"
#include "test.h"

#pragma c3po mangle(variadic)
const struct magic ** supercall(int j) {
    volatile int a = 0x4823;
    a *= 4;
    a <<= 2;
    a /= 3;
    a &= j;
    return NULL;
}

//this should also be edited but not passed params
void say_hi(const char *msg);

#pragma c3po mangle(variadic)
void say_hi(const char *msg) {
    volatile int a = 0;
    printf("%s\n", msg);
    a++;
}


#pragma c3po mangle(shuffle, name)
int scoper(int s, int v, ...)
{
#pragma c3po assert(s > 0)
#pragma c3po assert(v > 0)
    //so much
    (void)v;/* garbage */
    volatile int b = s + v;
    return b;
}

#pragma c3po mangle(shuffle)
void thing(int a, int *b, char c, char *d, double e, double *f);

//TODO currently unsupported
#pragma c3po mangle(shuffle)
void (*crazyfunc(int (a), int b, ...));

int main(int argc, char **argv) {
#pragma c3po assert(argc > 0)

    c3po_zero_elf();

    scoper(scoper(1, scoper(2, 3, 'c'), 'b', 'c', 'd'), 4, 'a', "hahaha");

#pragma c3po encrypt
#define tv1 "testing variadic"
#pragma c3po encrypt
#define tv2 "with multiple"
#pragma c3po encrypt
#define tv3 "calls"

    say_hi(tv1);
    say_hi(tv2);
    say_hi(tv3);

#pragma c3po encrypt
#define TESTING "testing stuff"

    printf("does this explode '%s'\n", TESTING);

    printf("does _this_ explode '%s'\n", TESTING);

#pragma c3po shatter(call, high, on)
    int i = 0;

#pragma c3po assert(i == 0)

    for (int j = 0; j < 40; ++j) {
#pragma c3po assert(j < 50)
        supercall(j);
    }

#pragma c3po shuffle(on)

    i += 3245;
    printf("decoded '%s'\n", BSTR);

#pragma c3po case

    i -= 32225;
    printf("decoded '%s'\n", CSTR);

#pragma c3po case

    i *= 345;
    puts("2");

#pragma c3po case

    printf("decoded '%s' and '%s'\n", BSTR, CSTR);

#pragma c3po case

    i <<= 3;
    puts("1");

#pragma c3po shuffle(off)

#pragma c3po assert(i != 0)
    printf("i:%d\n", i);

#pragma c3po shatter(off)

    return 0;
}
