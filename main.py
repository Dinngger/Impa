
import pygame
import math
from impa import Pos, Node, Map

m = Map()
with open('games/game1.txt', 'r') as f:
    lines = ''.join(f.readlines())
    print(lines)
    m.load(lines)

pygame.init()

size = (700, 700)
node_size = 30
off_set = ((700 - m.h * node_size) / 2.0, (700 - m.h * node_size) / 2.0)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("My Game")

colors = {0:(255, 0, 0), 1:(255, 255, 0), 2:(0, 0, 255)}
play = True

while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
    screen.fill((25, 25, 25))
    for i in range(m.h):
        for j in range(m.w):
            node = m.get(Pos(i, j))
            if node.valid:
                size = node_size / 2 * max(node.size, 0.2)
                block_offset = (node_size - size) / 2.0
                if node.type == 0:
                    pygame.draw.rect(screen, colors[node.color],
                                     [j * node_size + off_set[1] + block_offset,
                                      i * node_size + off_set[0] + block_offset, size, size])
    pygame.display.update()

print(m.success())
m.click(Pos(0, 0))
print(m.success())
