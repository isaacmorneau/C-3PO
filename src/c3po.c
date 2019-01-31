#include <elf.h>
#include <stdio.h>
#include <string.h>
#include <sys/mman.h>

#include "c3po.h"

inline void c3po_str_xor(const uint8_t *restrict encrypted, char *restrict decrypted, size_t len) {
    for (size_t i = 0; i < len; ++i) {
        decrypted[i] = encrypted[i] ^ encrypted[len + i];
    }
}


#pragma C3PO cxor enable
#define C3PO_SELFMAPS "/proc/self/maps\0 this is a lot more data to make sure its not optimized out"
#define C3PO_ADDRESS_MAPS "%llx-%llx"
#pragma C3PO cxor disable

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
