str1 = "Django allows a rapid web development and creates scalable systems"
str2 = "There are two areas in cloud computing: performance and security"

# Basic indexing/slicing
print(str1[9])          # single char at index 9
print(str2[-1:-6:-1])   # last char backwards 5 places
print(str2[-2:])        # last 2 chars
print(str2[0:20:3])     # every 3rd char from 0..19

# Concatenation with a space
print(str1 + " " + str2)

# Methods
print(str1.endswith("systems"))     # True/False
print(str2.split())                 # list of words
print(str1.upper(), str2.upper())   # uppercase versions
print(str1.replace("web", ""))      # remove "web"
print(str2.count('e'))              # occurrences of 'e'
