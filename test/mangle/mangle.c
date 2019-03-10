#include <stddef.h>
#pragma c3po mangle(name)
void t1(int foo, char *bar, char baz) {
}

#pragma c3po mangle(variadic)
void t2(int foo, char *bar, char baz) {
}

#pragma c3po mangle(shuffle)
void t3(int foo, char *bar, char baz) {
}

int main(void) {
    t1(1, NULL, 'a');
    t2(1, NULL, 'a');
    t3(1, NULL, 'a');
}
