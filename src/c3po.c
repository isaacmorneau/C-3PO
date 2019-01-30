#include "c3po.h"

void c3po_str_xor(const uint8_t *restrict encrypted, char *restrict decrypted, size_t len) {
    for (size_t i = 0; i < len; ++i) {
        decrypted[i] = encrypted[i] ^ encrypted[len + i];
    }
}
