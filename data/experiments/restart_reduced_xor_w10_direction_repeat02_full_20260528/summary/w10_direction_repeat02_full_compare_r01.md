# Reduced-XOR warmup10 full repeat02 vs run01

Complete repeat02 coverage for 8 data_ro and 8 except_ro directions. p1 is overall one probability over 1000 x 1000 bit-symbol restart output.

| label | p1 run01 | p1 run02 | delta | same sign | minH run01 | minH run02 |
| --- | ---: | ---: | ---: | --- | ---: | ---: |
| data_ro0 | 0.191877 | 0.182267 | -0.009610 | true | 0.307353 | 0.290298 |
| data_ro1 | 0.518915 | 0.522621 | +0.003706 | true | 0.946430 | 0.936163 |
| data_ro2 | 0.244002 | 0.245911 | +0.001909 | true | 0.403546 | 0.407193 |
| data_ro3 | 0.671833 | 0.671545 | -0.000288 | true | 0.573825 | 0.574444 |
| data_ro4 | 0.424639 | 0.427625 | +0.002986 | true | 0.797461 | 0.804967 |
| data_ro5 | 0.409454 | 0.405413 | -0.004041 | true | 0.759879 | 0.750040 |
| data_ro6 | 0.375380 | 0.375746 | +0.000366 | true | 0.678949 | 0.679795 |
| data_ro7 | 0.549958 | 0.547275 | -0.002683 | true | 0.862607 | 0.869662 |
| except_ro0 | 0.501020 | 0.500956 | -0.000064 | true | 0.997060 | 0.997244 |
| except_ro1 | 0.550312 | 0.553538 | +0.003226 | true | 0.861678 | 0.853246 |
| except_ro2 | 0.499674 | 0.499543 | -0.000131 | true | 0.999060 | 0.998682 |
| except_ro3 | 0.553930 | 0.553217 | -0.000713 | true | 0.852224 | 0.854083 |
| except_ro4 | 0.520205 | 0.519451 | -0.000754 | true | 0.942848 | 0.944940 |
| except_ro5 | 0.565521 | 0.566377 | +0.000856 | true | 0.822347 | 0.820165 |
| except_ro6 | 0.501833 | 0.500471 | -0.001362 | true | 0.994721 | 0.998642 |
| except_ro7 | 0.542602 | 0.542643 | +0.000041 | true | 0.882034 | 0.881925 |

## Summary

| mode | n | Pearson p1 | mean abs delta | max abs delta | max delta label | same sign | mean abs bias run01 | mean abs bias run02 |
| --- | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: |
| data_ro | 8 | 0.999678 | 0.003199 | 0.009610 | data_ro0 | 8/8 | 0.136919 | 0.138060 |
| except_data_ro | 8 | 0.999013 | 0.000893 | 0.003226 | except_ro1 | 8/8 | 0.029469 | 0.029639 |
