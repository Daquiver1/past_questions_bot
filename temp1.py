import re

name = input("Please enter your name: ")

#print(res)
if len(name.split()) == 1:
	temp = re.compile("([a-zA-Z]+)([0-9]+)")
	res = temp.match(name).groups()
else:
	res = name.split()


print(res[0])
print(res[1])

print(str(1+2) + "yaw")