# Sample lists
list1 = ["apple", 10, 3.14, [1, 2, 3], "class", 20, [4.5, 6.7], 5.5]
list2 = [8, "list in python", [9.1, 7.2], 15, "MAC", [2, 4, 6], 3.33, 12.5]

# Indexing into a nested list
print(list1[3][1])      # -> 2

# Negative indexing (last item)
print(list2[-1])        # -> 12.5

# Slicing: start:stop (stop not included)
print(list1[2:5])       # -> [3.14, [1, 2, 3], 'class']

# Step slicing: every other element
print(list2[0:7:2])     # -> [8, [9.1, 7.2], 'MAC', 3.33]

# Concatenation & repetition
print(list1 + list2)    # new list with items of both
print(list1 * 2)        # repeats items

# Safe element update inside a nested list
list2[5][1] = 0         # change middle of [2, 4, 6] -> [2, 0, 6]
print(list2[5])

# Delete by index
del list1[-3]           # removes the 3rd from the end
print(list1)

# Methods: append, pop, insert, extend
list1.append('university')
print(list1[-1])        # -> 'university'

removed = list2.pop()   # removes and returns last element
print("Popped:", removed)

list1.insert(5, 100)    # puts 100 at index 5
print(list1[5])

list2.extend([44, 50])  # add multiple items at the end
print(list2[-2:])
