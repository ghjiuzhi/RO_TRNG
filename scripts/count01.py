# def count_bits_in_file(file_path):
#     count_0 = 0
#     count_1 = 0

#     with open(file_path, 'rb') as file:
#         byte = file.read(1)
#         while byte:
#             # Convert byte to binary string
#             bits = bin(ord(byte))[2:].zfill(8)
#             count_0 += bits.count('0')
#             count_1 += bits.count('1')
#             byte = file.read(1)

#     return count_0, count_1

# # 使用示例
# file_path = '../sim/single/fro2sro3.DAT'
# count_0, count_1 = count_bits_in_file(file_path)
# p = count_1 / (count_0 + count_1)
# print(f"Number of 0s: {count_0}")
# print(f"Number of 1s: {count_1}")
# print(f"p = {p:.32f}")

with open(r"E:\Project\MLDSA\RO_TRNG\sim\2fro2_1sro9.DAT", "rb") as f:
    data = f.read()
#with open("E:/Project/MLDSA/RO_TRNG/data/lutl/RO2.DAT", "rb") as f:  
#     data = f.read()    
bitstring = ''.join(f'{byte:08b}' for byte in data)
ones = bitstring.count('1')
total = len(bitstring)
p = ones / total
print(f"p = {p:.6f}")