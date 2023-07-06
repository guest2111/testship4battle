

# G - ship
# @ - ship, if last hit
# o - hit before / empty
# O - last hit if on water
# x - targeted


# https://docs.python.org/3/library/string.html#string.ascii_lowercase
from string import ascii_lowercase as letters


size = 10
numspacer = str(size).__len__()+1
numspacer = ''.join(numspacer*[' '])
linelength = size*2 + 4
# emptyLine = ''.join([(size*2 + 3)*' ']) + '\n'
emptyLine = numspacer + ' '.join(letters)
emptyLine = emptyLine[:2+2*size] + numspacer
line = ' ' + ''.join([size*' .']) + ' '
field = emptyLine + size*line + emptyLine


field = []
for i,letter in enumerate(letters):
    if i > size + 1: break
    elif i == 0: field.append(emptyLine)
    elif i == 1 + size: field.append(emptyLine)
    else:
        line = [str.rjust(str(i),2),' '.join(size*['.']),str.ljust(str(i),2)]
        line = ' '.join(line)
        field.append(line)

print('\n'.join(field))

size = 9
linelength = size*2 + 4
line = ' ' + ''.join([size*' .']) + '  \n'
emptyLine = ''.join([(size*2 + 3)*' ']) + '\n'
field = emptyLine + size*line + emptyLine


print(field)



