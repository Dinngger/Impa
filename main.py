#!/usr/bin/python3
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from impa import Pos, Node, Map

games = {}
def get_game(i):
    if i not in games:
        tmp = Map()
        with open(f'games/game{i}.txt', 'r') as f:
            lines = ''.join(f.readlines())
            tmp.load(lines)
        games[i] = tmp
    return games[i]

pygame.init()

if os.path.exists('build/cache.txt'):
    with open('build/cache.txt', 'r') as f:
        game_id = int(f.readline())
else:
    game_id = 1
size = (700, 700)
node_size = 80
bg_size = node_size * 0.9
bg_offset = node_size * 0.05
screen = pygame.display.set_mode(size)
icon = pygame.image.load('assets/appicon.webp')
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
pygame.display.set_caption(f"IMPA - Level {game_id}")

colors = [(252, 142, 181), (253, 220, 139), (123, 170, 238)]
shadow_colors = [(172, 62, 99), (123, 97, 48), (39, 68, 110)]
botton_colors = [(131, 79, 101), (162, 130, 69), (56, 88, 149)]
node_sizes = [0.1, 0.35, 0.75]
shadow_sizes = [0, 2, 4]
node_radius = [-1, 5, 10]
play = True

m = Map(get_game(game_id))
off_set = ((700 - m.h * node_size) / 2.0, (700 - m.w * node_size) / 2.0)
refresh = True

while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            i = (y - off_set[0] - bg_offset) / node_size
            j = (x - off_set[1] - bg_offset) / node_size
            if i > 0 and i < m.h and i - int(i) < 0.9 and \
               j > 0 and j < m.w and j - int(j) < 0.9:
                m.click(Pos(int(i), int(j)))
            if m.success() and x > 120 and x < 200 and y > 40 and y < 120:
                game_id += 1
                with open('build/cache.txt', 'w') as f:
                    f.write(str(game_id))
                pygame.display.set_caption(f"IMPA - Level {game_id}")
                m = Map(get_game(game_id))
            if x > 40 and x < 120 and y > 40 and y < 120:
                m = Map(get_game(game_id))
            off_set = ((700 - m.h * node_size) / 2.0, (700 - m.w * node_size) / 2.0)
            refresh = True
    clock.tick(60)
    if not refresh:
        continue
    refresh = False
    screen.fill((41, 40, 46))
    pygame.draw.circle(screen, (172, 62, 99), (80, 85), 30)
    pygame.draw.circle(screen, (252, 142, 181), (80, 80), 30)
    if m.success():
        pygame.draw.circle(screen, (123, 97, 48), (160, 85), 30)
        pygame.draw.circle(screen, (253, 220, 139), (160, 80), 30)
    for i in range(m.h):
        for j in range(m.w):
            node = m.get(Pos(i, j))
            if node.valid:
                size = node_size * node_sizes[node.size]
                block_offset = (node_size - size) / 2.0
                if node.type in [0, 2, 3]:
                    pygame.draw.rect(screen, botton_colors[node.color],
                                     [j * node_size + off_set[1] + bg_offset,
                                      i * node_size + off_set[0] + bg_offset, bg_size, bg_size],
                                     border_radius=15)
                elif node.type == 1 and node.another_pos.x >= 0 and node.another_pos.y >=0:
                    rect_size_x, rect_size_y = bg_size, bg_size + node_size
                    if node.another_pos.y > 0:
                        rect_size_x, rect_size_y = rect_size_y, rect_size_x
                    pygame.draw.rect(screen, botton_colors[node.color],
                                     [j * node_size + off_set[1] + bg_offset,
                                      i * node_size + off_set[0] + bg_offset,
                                      rect_size_x, rect_size_y], border_radius=15)
                if node.type == 2:
                    pygame.draw.rect(screen, colors[node.next_color],
                                     [j * node_size + off_set[1] + bg_offset,
                                      i * node_size + off_set[0] + bg_offset, bg_size, bg_size],
                                     width=2, border_radius=15)
                if node.size > 0:
                    pygame.draw.rect(screen, shadow_colors[node.color],
                                    [j * node_size + off_set[1] + block_offset,
                                    i * node_size + off_set[0] + block_offset
                                    + shadow_sizes[node.size], size, size],
                                    border_radius=node_radius[node.size])
                pygame.draw.rect(screen, colors[node.color],
                                 [j * node_size + off_set[1] + block_offset,
                                  i * node_size + off_set[0] + block_offset
                                  - shadow_sizes[node.size], size, size],
                                 border_radius=node_radius[node.size])
    pygame.display.flip()
