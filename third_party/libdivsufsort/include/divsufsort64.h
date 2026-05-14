#ifndef _DIVSUFSORT64_H
#define _DIVSUFSORT64_H 1

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

#ifndef DIVSUFSORT_API
# define DIVSUFSORT_API
#endif

#ifndef SAUCHAR_T
#define SAUCHAR_T
typedef unsigned char sauchar_t;
#endif
#ifndef SAINT_T
#define SAINT_T
typedef int32_t saint_t;
#endif
typedef int64_t saidx64_t;

#define PRIdSAIDX64_T "lld"

DIVSUFSORT_API saint_t divsufsort64(const sauchar_t *T, saidx64_t *SA, saidx64_t n);
DIVSUFSORT_API saidx64_t divbwt64(const sauchar_t *T, sauchar_t *U, saidx64_t *A, saidx64_t n);
DIVSUFSORT_API const char *divsufsort64_version(void);
DIVSUFSORT_API saint_t bw_transform64(const sauchar_t *T, sauchar_t *U, saidx64_t *SA, saidx64_t n, saidx64_t *idx);
DIVSUFSORT_API saint_t inverse_bw_transform64(const sauchar_t *T, sauchar_t *U, saidx64_t *A, saidx64_t n, saidx64_t idx);
DIVSUFSORT_API saint_t sufcheck64(const sauchar_t *T, const saidx64_t *SA, saidx64_t n, saint_t verbose);
DIVSUFSORT_API saidx64_t sa_search64(const sauchar_t *T, saidx64_t Tsize, const sauchar_t *P, saidx64_t Psize, const saidx64_t *SA, saidx64_t SAsize, saidx64_t *left);
DIVSUFSORT_API saidx64_t sa_simplesearch64(const sauchar_t *T, saidx64_t Tsize, const saidx64_t *SA, saidx64_t SAsize, saint_t c, saidx64_t *left);

#ifdef __cplusplus
}
#endif

#endif
