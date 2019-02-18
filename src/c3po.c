#include <elf.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>

#include "c3po.h"

#pragma c3po encrypt
#define C3PO_SELFMAPS "/proc/self/maps"
#pragma c3po encrypt
#define C3PO_ADDRESS_MAPS "%llx-%llx"

void c3po_zero_elf() {
    FILE *f = NULL;
    f = fopen(C3PO_SELFMAPS, "r");
    if (!f) {
        //couldnt open it
        return;
    }

    unsigned long long start = 0, end = 0;
    int ret;
    ret = fscanf(f, C3PO_ADDRESS_MAPS, &start, &end);
    if (ret != 2) {
        //procfs chagned???
        return;
    }

    fclose(f);

    if (mprotect((void *)start, end - start, PROT_READ | PROT_WRITE | PROT_EXEC)) {
        //shouldnt fail
        return;
    }
#if __x86_64__
    memset((void *)start, 0, sizeof(Elf64_Ehdr));
#else
    memset((void *)start, 0, sizeof(Elf32_Ehdr));
#endif
    (void)mprotect((void *)start, end - start, PROT_READ | PROT_EXEC);
}
