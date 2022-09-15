import multiprocessing

array = [1, 2, 3, 4, 5, 6]
dictt = [{"a": 11}, {"b": 12}, {"c": 13}, {"d": 14}, {"e": 15}]

# for x, y in zip(array, dictt):
#     for z in y:
#         if 'b' in y:
#             print('SIema', y)
#         print(x, z, y[z])

# if 'b' in dictt

# for x in dictt[0]:
#     print(x)
# for i in range(len(dictt)):
#     if 'b' in dictt[i]:
#         print('asd', dictt[i])

print(dictt[1].get('b'))

print("Number of cpu : ", multiprocessing.cpu_count())