# Literal
d1 = {"name": "Bob", "age": 35, (4, 10): ['x', 'y', 'z'], "+1": "Canada", 44: 99, 19: 555}

# From sequence of pairs
d2 = dict([("name", "Livy"), ("age", 44), ((1, 3, 5), ['a', 'b', 'c']), (0, 'black'), (33, 67)])

# Using keywords
d3 = dict(id=2277, name='Michael', siblings=['Janet', 'Martin', 'Richard'])

# Core lookups
print(d1.keys())                 # view of keys
print(d2.values())               # view of values
print(d3.get('id'))              # 2277
print(d2.get('age'))             # 44
print(d3.get('age'))             # None (not present)
print(d3.get('name', 'Tim'))     # 'Michael' (fallback not used)

# Items and indexing
print(d2.items())                # (key, value) pairs
print(d3['siblings'])            # list of names

# Safe get for missing composite key
print(d1.get((1, 2)))            # None (doesn't exist)

# Merge/update: after this, d2 will have keys from d3
d2.update(d3)
print(d2['name'])                # 'Michael' (overwritten)
print(d2.get('siblings'))        # now present

# Comparisons and length
print(d1 == d2)                  # likely False
print(len(d2))                   # number of keys

# Iterate keys/values
for k in d1.keys():
    print("k:", k)

for k in d2.keys():
    print("v:", d2[k])

