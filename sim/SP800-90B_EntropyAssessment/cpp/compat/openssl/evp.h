#ifndef RO_TRNG_COMPAT_OPENSSL_EVP_H
#define RO_TRNG_COMPAT_OPENSSL_EVP_H

#include <windows.h>
#include <wincrypt.h>
#include "sha.h"

#ifndef ALG_SID_SHA_256
#define ALG_SID_SHA_256 12
#endif

#ifndef CALG_SHA_256
#define CALG_SHA_256 (ALG_CLASS_HASH | ALG_TYPE_ANY | ALG_SID_SHA_256)
#endif

struct EVP_MD_CTX {
    HCRYPTPROV provider;
    HCRYPTHASH hash;
};

struct EVP_MD {
    int dummy;
};

inline EVP_MD_CTX *EVP_MD_CTX_new(void) {
    EVP_MD_CTX *ctx = new EVP_MD_CTX();
    ctx->provider = 0;
    ctx->hash = 0;
    return ctx;
}

inline void EVP_MD_CTX_free(EVP_MD_CTX *ctx) {
    if (!ctx) {
        return;
    }
    if (ctx->hash) {
        CryptDestroyHash(ctx->hash);
    }
    if (ctx->provider) {
        CryptReleaseContext(ctx->provider, 0);
    }
    delete ctx;
}

inline const EVP_MD *EVP_sha256(void) {
    static EVP_MD md = {0};
    return &md;
}

inline int EVP_DigestInit_ex(EVP_MD_CTX *ctx, const EVP_MD *, void *) {
    if (!ctx) {
        return 0;
    }
    if (!CryptAcquireContext(&ctx->provider, NULL, NULL, PROV_RSA_AES, CRYPT_VERIFYCONTEXT)) {
        if (!CryptAcquireContext(&ctx->provider, NULL, NULL, PROV_RSA_FULL, CRYPT_VERIFYCONTEXT)) {
            return 0;
        }
    }
    if (!CryptCreateHash(ctx->provider, CALG_SHA_256, 0, 0, &ctx->hash)) {
        return 0;
    }
    return 1;
}

inline int EVP_DigestUpdate(EVP_MD_CTX *ctx, const void *data, size_t count) {
    if (!ctx || !ctx->hash) {
        return 0;
    }
    return CryptHashData(ctx->hash, const_cast<BYTE *>(static_cast<const BYTE *>(data)), static_cast<DWORD>(count), 0) ? 1 : 0;
}

inline int EVP_DigestFinal_ex(EVP_MD_CTX *ctx, unsigned char *digest, unsigned int *digest_len) {
    if (!ctx || !ctx->hash || !digest) {
        return 0;
    }
    DWORD len = SHA256_DIGEST_LENGTH;
    if (!CryptGetHashParam(ctx->hash, HP_HASHVAL, digest, &len, 0)) {
        return 0;
    }
    if (digest_len) {
        *digest_len = static_cast<unsigned int>(len);
    }
    return 1;
}

#endif
