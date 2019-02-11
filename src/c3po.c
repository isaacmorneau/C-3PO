#include <elf.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>

#include "c3po.h"

void c3po_str_xor(const uint8_t *restrict base, uint8_t *restrict key1, const uint8_t *restrict key2,
    char *decrypted, size_t len) {

    for (size_t i = 0; i < len; ++i) {
        key1[i] ^= key2[i];
    }

    for (size_t i = 0; i < len; ++i) {
        decrypted[i] = base[i] ^ key1[i];
    }

    for (size_t i = 0; i < len; ++i) {
        key1[i] ^= key2[i];
    }
}

#pragma c3po cxor(on, 64)
#define C3PO_SELFMAPS "/proc/self/maps"
#define C3PO_ADDRESS_MAPS "%llx-%llx"
#pragma c3po cxor(off)

void c3po_zero_elf() {
    FILE *f = NULL;
    C3PO_STR(f = fopen(c3po_str, "r"), C3PO_SELFMAPS);
    if (!f) {
        //couldnt open it
        return;
    }

    unsigned long long start = 0, end = 0;
    int ret;
    C3PO_STR(ret = fscanf(f, c3po_str, &start, &end), C3PO_ADDRESS_MAPS);
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
