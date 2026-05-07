# A slightly richer nested-loop demo (right triangle of numbers)
# 1
# 1 2
# 1 2 3
rows = 3
for r in range(1, rows + 1):
    line = ""
    for c in range(1, r + 1):
        line += str(c) + " "
    print(line.strip())
