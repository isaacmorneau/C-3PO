#include <stdio.h>

int main(int argc, char **argv) {
    (void)argv;
#pragma c3po assert(argc > 0)

    for (int i = 0; i < 10; ++i) {
#pragma c3po assert(i < 10)
        printf("%d", i);
#pragma c3po assert(i >= 0)
    }
}
