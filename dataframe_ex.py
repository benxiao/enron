from pandas import DataFrame


data = {
    'a': [1, 2],
    'b': [3, 4]
}

data2 = [[1,2,3,4], [4,5,6,7]]

df = DataFrame(data, columns=['b', 'a']) # guarantee the order of the columns
print(df)

df2 = DataFrame(data2,columns=['a', 'c', 'b', 'd'])
print(df2)

data3 = [('a', 'b'),(1,2),(3,4)]
df3 = DataFrame(data3[1:], columns=data3[0])
print(df3)


data4 = [('a', 'b'), ('c', 'd')]
df4 = DataFrame(data4)
print(df4)
print(df4.values)
print(type(df4.values))
print(df4.values.tolist())
