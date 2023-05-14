i=0
file = open('./assets/text/help.txt', 'r')
Lines = file.readlines()
for line in Lines:
	print(i)
	print(line)
	i+=10