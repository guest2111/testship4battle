

# G - ship
# @ - ship, if last hit
# o - hit before / empty
# O - last hit if on water
# x - targeted

from fastapi import FastAPI

app = FastAPI()



# https://docs.python.org/3/library/string.html#string.ascii_lowercase
from string import ascii_lowercase as letters
import subprocess
from pynput import keyboard


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

# https://pynput.readthedocs.io/en/latest/keyboard.html
# https://stackoverflow.com/questions/49578801/preventing-key-presses-from-appearing-on-screen


def echooff():
    subprocess.run(['stty', '-echo'], check=True)


def echoon():
    subprocess.run(['stty', 'echo'], check=True)

# global x, y
x,y = [0, 0]
x = 0
y = size + 1
def echo_disabled():
    try:
        echooff()
        yield
    finally:
        echoon()


def on_press(key):
    try:
        print('{0} pushed'.format(
        key.name))
    except:
        print('{0} pushed'.format(
        key))
    try:
        # print('alphanumeric key {0} pressed'.format(
        #     key.char))
        pass
    except AttributeError:
        print('special key {0} pressed'.format(
            key))


def on_release(key):
    global x, y, size, linelength, field
    print('{0} released'.format(
        key))
    print(key.__dir__())
    print(type(key))
    try:
        print(key.name)
        if key.name == 'space':
            index = linelength*y+2*x
            field = field[:index] + 'o' + field[index+1:]
        if key.name == 'right':
            x += 1
        if key.name == 'left':
            x -= 1
        if key.name == 'up':
            y -= 1
        if key.name == 'down':
            y += 1
    except: 
        print(f'key {key.char} was pushed')
        pass
    # print(key.value)
    if y > 1 + size: y -= 1
    if x*2 + 1 > linelength: x -= 1
    if x < 0: x = 0
    if y < 0: y = 0
    print(f'position: ({x},{y})')
    output = field
    index = linelength*y+2*x
    output = output[:index] + 'x' + output[index+1:]
    print(output)
    if key == keyboard.Key.esc:
        # Stop listener
        return False


@app.get("/")
def root():
    try:
        echooff()
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()
    finally:
        echoon()

if __name__ == '__main__':
    root()
