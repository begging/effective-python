arr = [[1,2,3], [4,5,6], [7,8,9]]
flat = [x for row in arr for x in row]
print(flat)

squared = [[x**2 for x in row] for row in arr]
print(squared)

arr2 = [[[1, 2, 3], [4, 5, 6]]]
complicated_flat = [x for sublist1 in arr2
                        for sublist2 in sublist1
                            for x in sublist2]
print(complicated_flat)

desirable_flat = []
for sublist1 in arr2:
    for sublist2 in sublist1:
        desirable_flat.extend(sublist2)
print(desirable_flat)
