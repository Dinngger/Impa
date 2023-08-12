# import pygame
import impa

m = impa.Map()
with open('games/game1.txt', 'r') as f:
    lines = ''.join(f.readlines())
    print(lines)
    m.load(lines)

print(m.success())
m.click(0, 0)
print(m.success())
