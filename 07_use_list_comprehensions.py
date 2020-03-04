a = [1,2,3,4,5,6,7,8,9,10]

hard_to_read = map(lambda x: x**2, filter(lambda x: x % 2 == 0, a))
print(list(hard_to_read))

easy_to_read = [x**2 for x in a if x % 2 == 0]
print(easy_to_read)
