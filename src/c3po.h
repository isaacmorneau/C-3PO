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
#define AES256 1
#define AES_BLOCKLEN 16
#define AES_KEYLEN 32
#define AES_keyExpSize 240
struct AES_ctx {
    uint8_t RoundKey[AES_keyExpSize];
    uint8_t Iv[AES_BLOCKLEN];
};
void AES_init_ctx(struct AES_ctx *ctx, const uint8_t *key);
void AES_init_ctx_iv(struct AES_ctx *ctx, const uint8_t *key, const uint8_t *iv);
void AES_ctx_set_iv(struct AES_ctx *ctx, const uint8_t *iv);
void AES_CBC_encrypt_buffer(struct AES_ctx *ctx, uint8_t *buf, uint32_t length);
void AES_CBC_decrypt_buffer(struct AES_ctx *ctx, uint8_t *buf, uint32_t length);
