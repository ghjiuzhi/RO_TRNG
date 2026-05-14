#ifndef _LFS_H
#define _LFS_H 1

#include <stdio.h>

#define LFS_OFF_T long
#define LFS_FOPEN fopen
#define LFS_FTELL ftell
#define LFS_FSEEK fseek
#define LFS_PRId "ld"

#ifndef PRIdOFF_T
# define PRIdOFF_T LFS_PRId
#endif

#endif
