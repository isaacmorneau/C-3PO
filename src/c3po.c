#include <elf.h>
#include <stdint.h>
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
    f       = fopen(C3PO_SELFMAPS, "r");
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

//aes functionality
#define nb 4
#if defined(aes256) && (aes256 == 1)
#define nk 8
#define nr 14
#elif defined(aes192) && (aes192 == 1)
#define nk 6
#define nr 12
#else
#define nk 4
#define nr 10
#endif

typedef uint8_t state_t[4][4];
static const uint8_t sbox[256]  = {0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67,
    0x2b, 0xfe, 0xd7, 0xab, 0x76, 0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2,
    0xaf, 0x9c, 0xa4, 0x72, 0xc0, 0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5,
    0xf1, 0x71, 0xd8, 0x31, 0x15, 0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80,
    0xe2, 0xeb, 0x27, 0xb2, 0x75, 0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6,
    0xb3, 0x29, 0xe3, 0x2f, 0x84, 0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe,
    0x39, 0x4a, 0x4c, 0x58, 0xcf, 0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02,
    0x7f, 0x50, 0x3c, 0x9f, 0xa8, 0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda,
    0x21, 0x10, 0xff, 0xf3, 0xd2, 0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e,
    0x3d, 0x64, 0x5d, 0x19, 0x73, 0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8,
    0x14, 0xde, 0x5e, 0x0b, 0xdb, 0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac,
    0x62, 0x91, 0x95, 0xe4, 0x79, 0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4,
    0xea, 0x65, 0x7a, 0xae, 0x08, 0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74,
    0x1f, 0x4b, 0xbd, 0x8b, 0x8a, 0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57,
    0xb9, 0x86, 0xc1, 0x1d, 0x9e, 0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87,
    0xe9, 0xce, 0x55, 0x28, 0xdf, 0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d,
    0x0f, 0xb0, 0x54, 0xbb, 0x16};
static const uint8_t rsbox[256] = {0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3,
    0x9e, 0x81, 0xf3, 0xd7, 0xfb, 0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43,
    0x44, 0xc4, 0xde, 0xe9, 0xcb, 0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95,
    0x0b, 0x42, 0xfa, 0xc3, 0x4e, 0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2,
    0x49, 0x6d, 0x8b, 0xd1, 0x25, 0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c,
    0xcc, 0x5d, 0x65, 0xb6, 0x92, 0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46,
    0x57, 0xa7, 0x8d, 0x9d, 0x84, 0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58,
    0x05, 0xb8, 0xb3, 0x45, 0x06, 0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd,
    0x03, 0x01, 0x13, 0x8a, 0x6b, 0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf,
    0xce, 0xf0, 0xb4, 0xe6, 0x73, 0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37,
    0xe8, 0x1c, 0x75, 0xdf, 0x6e, 0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62,
    0x0e, 0xaa, 0x18, 0xbe, 0x1b, 0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0,
    0xfe, 0x78, 0xcd, 0x5a, 0xf4, 0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10,
    0x59, 0x27, 0x80, 0xec, 0x5f, 0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a,
    0x9f, 0x93, 0xc9, 0x9c, 0xef, 0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb,
    0x3c, 0x83, 0x53, 0x99, 0x61, 0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14,
    0x63, 0x55, 0x21, 0x0c, 0x7d};
static const uint8_t rcon[11] = {0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36};
#define getsboxvalue(num) (sbox[(num)])
#define getsboxinvert(num) (rsbox[(num)])
static void keyexpansion(uint8_t *roundkey, const uint8_t *key) {
    unsigned i, j, k;
    uint8_t tempa[4];
    for (i = 0; i < nk; ++i) {
        roundkey[(i * 4) + 0] = key[(i * 4) + 0];
        roundkey[(i * 4) + 1] = key[(i * 4) + 1];
        roundkey[(i * 4) + 2] = key[(i * 4) + 2];
        roundkey[(i * 4) + 3] = key[(i * 4) + 3];
    }
    for (i = nk; i < nb * (nr + 1); ++i) {
        {
            k        = (i - 1) * 4;
            tempa[0] = roundkey[k + 0];
            tempa[1] = roundkey[k + 1];
            tempa[2] = roundkey[k + 2];
            tempa[3] = roundkey[k + 3];
        }
        if (i % nk == 0) {
            {
                const uint8_t u8tmp = tempa[0];
                tempa[0]            = tempa[1];
                tempa[1]            = tempa[2];
                tempa[2]            = tempa[3];
                tempa[3]            = u8tmp;
            }
            {
                tempa[0] = getsboxvalue(tempa[0]);
                tempa[1] = getsboxvalue(tempa[1]);
                tempa[2] = getsboxvalue(tempa[2]);
                tempa[3] = getsboxvalue(tempa[3]);
            }
            tempa[0] = tempa[0] ^ rcon[i / nk];
        }
#if defined(aes256) && (aes256 == 1)
        if (i % nk == 4) {
            {
                tempa[0] = getsboxvalue(tempa[0]);
                tempa[1] = getsboxvalue(tempa[1]);
                tempa[2] = getsboxvalue(tempa[2]);
                tempa[3] = getsboxvalue(tempa[3]);
            }
        }
#endif
        j               = i * 4;
        k               = (i - nk) * 4;
        roundkey[j + 0] = roundkey[k + 0] ^ tempa[0];
        roundkey[j + 1] = roundkey[k + 1] ^ tempa[1];
        roundkey[j + 2] = roundkey[k + 2] ^ tempa[2];
        roundkey[j + 3] = roundkey[k + 3] ^ tempa[3];
    }
}
void aes_init_ctx_iv(struct aes_ctx *ctx, const uint8_t *key, const uint8_t *iv) {
    keyexpansion(ctx->roundkey, key);
    memcpy(ctx->iv, iv, aes_blocklen);
}
void aes_ctx_set_iv(struct aes_ctx *ctx, const uint8_t *iv) {
    memcpy(ctx->iv, iv, aes_blocklen);
}
static void addroundkey(uint8_t round, state_t *state, uint8_t *roundkey) {
    uint8_t i, j;
    for (i = 0; i < 4; ++i) {
        for (j = 0; j < 4; ++j) {
            (*state)[i][j] ^= roundkey[(round * nb * 4) + (i * nb) + j];
        }
    }
}
static void subbytes(state_t *state) {
    uint8_t i, j;
    for (i = 0; i < 4; ++i) {
        for (j = 0; j < 4; ++j) {
            (*state)[j][i] = getsboxvalue((*state)[j][i]);
        }
    }
}
static void shiftrows(state_t *state) {
    uint8_t temp;
    temp           = (*state)[0][1];
    (*state)[0][1] = (*state)[1][1];
    (*state)[1][1] = (*state)[2][1];
    (*state)[2][1] = (*state)[3][1];
    (*state)[3][1] = temp;
    temp           = (*state)[0][2];
    (*state)[0][2] = (*state)[2][2];
    (*state)[2][2] = temp;
    temp           = (*state)[1][2];
    (*state)[1][2] = (*state)[3][2];
    (*state)[3][2] = temp;
    temp           = (*state)[0][3];
    (*state)[0][3] = (*state)[3][3];
    (*state)[3][3] = (*state)[2][3];
    (*state)[2][3] = (*state)[1][3];
    (*state)[1][3] = temp;
}
static uint8_t xtime(uint8_t x) {
    return ((x << 1) ^ (((x >> 7) & 1) * 0x1b));
}
static void mixcolumns(state_t *state) {
    uint8_t i;
    uint8_t tmp, tm, t;
    for (i = 0; i < 4; ++i) {
        t   = (*state)[i][0];
        tmp = (*state)[i][0] ^ (*state)[i][1] ^ (*state)[i][2] ^ (*state)[i][3];
        tm  = (*state)[i][0] ^ (*state)[i][1];
        tm  = xtime(tm);
        (*state)[i][0] ^= tm ^ tmp;
        tm = (*state)[i][1] ^ (*state)[i][2];
        tm = xtime(tm);
        (*state)[i][1] ^= tm ^ tmp;
        tm = (*state)[i][2] ^ (*state)[i][3];
        tm = xtime(tm);
        (*state)[i][2] ^= tm ^ tmp;
        tm = (*state)[i][3] ^ t;
        tm = xtime(tm);
        (*state)[i][3] ^= tm ^ tmp;
    }
}
#define multiply(x, y)                                                            \
    (((y & 1) * x) ^ ((y >> 1 & 1) * xtime(x)) ^ ((y >> 2 & 1) * xtime(xtime(x))) \
        ^ ((y >> 3 & 1) * xtime(xtime(xtime(x))))                                 \
        ^ ((y >> 4 & 1) * xtime(xtime(xtime(xtime(x))))))
static void invmixcolumns(state_t *state) {
    int i;
    uint8_t a, b, c, d;
    for (i = 0; i < 4; ++i) {
        a = (*state)[i][0];
        b = (*state)[i][1];
        c = (*state)[i][2];
        d = (*state)[i][3];
        (*state)[i][0]
            = multiply(a, 0x0e) ^ multiply(b, 0x0b) ^ multiply(c, 0x0d) ^ multiply(d, 0x09);
        (*state)[i][1]
            = multiply(a, 0x09) ^ multiply(b, 0x0e) ^ multiply(c, 0x0b) ^ multiply(d, 0x0d);
        (*state)[i][2]
            = multiply(a, 0x0d) ^ multiply(b, 0x09) ^ multiply(c, 0x0e) ^ multiply(d, 0x0b);
        (*state)[i][3]
            = multiply(a, 0x0b) ^ multiply(b, 0x0d) ^ multiply(c, 0x09) ^ multiply(d, 0x0e);
    }
}
static void invsubbytes(state_t *state) {
    uint8_t i, j;
    for (i = 0; i < 4; ++i) {
        for (j = 0; j < 4; ++j) {
            (*state)[j][i] = getsboxinvert((*state)[j][i]);
        }
    }
}
static void invshiftrows(state_t *state) {
    uint8_t temp;
    temp           = (*state)[3][1];
    (*state)[3][1] = (*state)[2][1];
    (*state)[2][1] = (*state)[1][1];
    (*state)[1][1] = (*state)[0][1];
    (*state)[0][1] = temp;
    temp           = (*state)[0][2];
    (*state)[0][2] = (*state)[2][2];
    (*state)[2][2] = temp;
    temp           = (*state)[1][2];
    (*state)[1][2] = (*state)[3][2];
    (*state)[3][2] = temp;
    temp           = (*state)[0][3];
    (*state)[0][3] = (*state)[1][3];
    (*state)[1][3] = (*state)[2][3];
    (*state)[2][3] = (*state)[3][3];
    (*state)[3][3] = temp;
}
static void cipher(state_t *state, uint8_t *roundkey) {
    uint8_t round = 0;
    addroundkey(0, state, roundkey);
    for (round = 1; round < nr; ++round) {
        subbytes(state);
        shiftrows(state);
        mixcolumns(state);
        addroundkey(round, state, roundkey);
    }
    subbytes(state);
    shiftrows(state);
    addroundkey(nr, state, roundkey);
}
static void invcipher(state_t *state, uint8_t *roundkey) {
    uint8_t round = 0;
    addroundkey(nr, state, roundkey);
    for (round = (nr - 1); round > 0; --round) {
        invshiftrows(state);
        invsubbytes(state);
        addroundkey(round, state, roundkey);
        invmixcolumns(state);
    }
    invshiftrows(state);
    invsubbytes(state);
    addroundkey(0, state, roundkey);
}
static void xorwithiv(uint8_t *buf, uint8_t *iv) {
    uint8_t i;
    for (i = 0; i < aes_blocklen; ++i) {
        buf[i] ^= iv[i];
    }
}
void aes_cbc_encrypt_buffer(struct aes_ctx *ctx, uint8_t *buf, uint32_t length) {
    uintptr_t i;
    uint8_t *iv = ctx->iv;
    for (i = 0; i < length; i += aes_blocklen) {
        xorwithiv(buf, iv);
        cipher((state_t *)buf, ctx->roundkey);
        iv = buf;
        buf += aes_blocklen;
    }
    memcpy(ctx->iv, iv, aes_blocklen);
}
void aes_cbc_decrypt_buffer(struct aes_ctx *ctx, uint8_t *buf, uint32_t length) {
    uintptr_t i;
    uint8_t storenextiv[aes_blocklen];
    for (i = 0; i < length; i += aes_blocklen) {
        memcpy(storenextiv, buf, aes_blocklen);
        invcipher((state_t *)buf, ctx->roundkey);
        xorwithiv(buf, ctx->iv);
        memcpy(ctx->iv, storenextiv, aes_blocklen);
        buf += aes_blocklen;
    }
}
