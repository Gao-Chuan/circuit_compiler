# 清零a的空间、为a赋值3
2 1 0 0 XOR
2 1 1 1 XOR
2 1 2 2 XOR
2 1 3 3 XOR
2 1 4 4 XOR
2 1 5 5 XOR
2 1 6 6 XOR
2 1 7 7 XOR
1 1 0 0 INV
1 1 1 1 INV
# 清零b的空间、为b赋值7
2 1 8 8 XOR
2 1 9 9 XOR
2 1 10 10 XOR
2 1 11 11 XOR
2 1 12 12 XOR
2 1 13 13 XOR
2 1 14 14 XOR
2 1 15 15 XOR
1 1 8 8 INV
1 1 9 9 INV
1 1 10 10 INV
# 清零c的空间、为c赋值9
2 1 16 16 XOR
2 1 17 17 XOR
2 1 18 18 XOR
2 1 19 19 XOR
2 1 20 20 XOR
2 1 21 21 XOR
2 1 22 22 XOR
2 1 23 23 XOR
1 1 16 16 INV
1 1 19 19 INV
# 0号中间变量，赋值为a^b。（因为所有的中间变量只被使用一次，所以不需要在赋值前清零）
2 1 0 8 24 XOR
2 1 1 9 25 XOR
2 1 2 10 26 XOR
2 1 3 11 27 XOR
2 1 4 12 28 XOR
2 1 5 13 29 XOR
2 1 6 14 30 XOR
2 1 7 15 31 XOR
# 将0号中间变量上的值传给c（使用两个INV传递一位）
1 1 24 16 INV
1 1 16 16 INV
1 1 25 17 INV
1 1 17 17 INV
1 1 26 18 INV
1 1 18 18 INV
1 1 27 19 INV
1 1 19 19 INV
1 1 28 20 INV
1 1 20 20 INV
1 1 29 21 INV
1 1 21 21 INV
1 1 30 22 INV
1 1 22 22 INV
1 1 31 23 INV
1 1 23 23 INV


# reserved = {
#     'if': 'IF',
#     'then': 'THEN',
#     'else': 'ELSE'
# }


# print(reserved.get('ifs', 'ID'))
