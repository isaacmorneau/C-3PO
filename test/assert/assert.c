#include <stdio.h>

int main(int argc, char **argv) {
    (void)argv;
#pragma c3po assert(argc > 0)
    for (int i = 0; i < 10; ++i) {
        printf("%d", i);
    }
}
