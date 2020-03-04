# The values before and after the assigned slice will be preserved.
# The list will grow or shrink to accommodate the new values.
a = [0,1,2,3,4,5,6,7,8,9]
print('Before', a)
a[2:7] = ['a','b','c']
print('After', a)
