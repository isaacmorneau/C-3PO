#pragma once
#include <stddef.h>
#include <stdint.h>

//a wonderful hack from the talk by int0x80 on anti forensics AF - defcon 24
//this little mess is designed to cause issues for automated analysis tools
#pragma c3po mangle(name)
void c3po_zero_elf();

//AES functionality
//stripped and included from: https://github.com/kokke/tiny-AES-c
#include <stdint.h>
#define aes256 1
#define aes_blocklen 16
#define aes_keylen 32
#define aes_keyexpsize 240
struct aes_ctx {
    uint8_t roundkey[aes_keyexpsize];
    uint8_t iv[aes_blocklen];
};
#pragma c3po mangle(name)
void aes_init_ctx_iv(struct aes_ctx *ctx, const uint8_t *key, const uint8_t *iv);
#pragma c3po mangle(name)
void aes_ctx_set_iv(struct aes_ctx *ctx, const uint8_t *iv);
#pragma c3po mangle(name)
void aes_cbc_encrypt_buffer(struct aes_ctx *ctx, uint8_t *buf, uint32_t length);
#pragma c3po mangle(name)
void aes_cbc_decrypt_buffer(struct aes_ctx *ctx, uint8_t *buf, uint32_t length);
